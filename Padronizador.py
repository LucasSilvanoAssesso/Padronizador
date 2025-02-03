import unicodedata
import argparse
import time
from string import printable
import pandas as pd
import chardet
import os

def get_only_characters(texts):
    if texts is None or pd.isna(texts):
        return ""
    if isinstance(texts, bytes):
        texts = texts.decode('utf-8', 'ignore')
    elif not isinstance(texts, str):
        texts = str(texts)
    
    textos_normalizados = unicodedata.normalize('NFC', texts)
    return ''.join(char for char in textos_normalizados if char in printable or char.isprintable())

def gerar_nome_saida(input_file):
    """
    Gera o nome do arquivo de saída adicionando '_Tratado' antes da extensão.
    """
    base, ext = os.path.splitext(input_file)
    return f"{base}_Tratado{ext}"

def process_csv(input_file):
    try:
        start_time = time.time()
        
        with open(input_file, 'rb') as f:
            raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding']
            if encoding is None:
                encoding = 'utf-8'

        arquivo_saida = gerar_nome_saida(input_file)
        
        with open(input_file, 'r', encoding=encoding) as entrada, open(arquivo_saida, 'w', encoding=encoding) as saida:
            linha_em_processo = ''
            linha_contador = 0
            for linha in entrada:
                linha = linha.strip()
                linha_em_processo += linha
                if linha_em_processo.count('<>') >= 25:
                    linha_em_processo = get_only_characters(linha_em_processo)
                    linha_em_processo = linha_em_processo.replace('"', ' ')
                    campos = linha_em_processo.split('<>')
                    if len(campos) > 5:
                        campos[5] = campos[5].replace(' ', '')
                    campos_com_aspas = [f'"{campo.strip()}"' if campo.strip() != '' else '""' for campo in campos]
                    linha_formatada = ';'.join(campos_com_aspas)
                    saida.write(linha_formatada + '\n')
                    linha_em_processo = ''
                    linha_contador += 1
        
        end_time = time.time()
        print(f"Arquivo processado e salvo como: {arquivo_saida}")
        print(f"Número total de linhas processadas: {linha_contador}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para processar arquivos CSV")
    parser.add_argument("input_csv", help="Caminho do arquivo CSV de entrada")
    args = parser.parse_args()
    process_csv(args.input_csv)
