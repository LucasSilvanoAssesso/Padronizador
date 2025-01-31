import unicodedata
from string import printable
import pandas as pd
import chardet
import os

def get_only_characters(texts):
    """
    Remove caracteres não imprimíveis de um texto, mantendo caracteres acentuados e válidos.
    """
    if texts is None or pd.isna(texts):
        return ""

    if isinstance(texts, bytes):
        texts = texts.decode('utf-8', 'ignore')
    elif isinstance(texts, str):
        pass
    else:
        texts = str(texts)
    
    # Normaliza para remover apenas caracteres não imprimíveis, mantendo acentos
    textos_normalizados = unicodedata.normalize('NFC', texts)
    
    # Filtra apenas os caracteres imprimíveis
    resultado = ''.join(char for char in textos_normalizados if char in printable or char.isprintable())
    return resultado

def gerar_nome_saida(input_file):
    """
    Gera o nome do arquivo de saída adicionando '_Tratado' antes da extensão.
    """
    base, ext = os.path.splitext(input_file)
    return f"{base}_Tratado{ext}"

def process_csv(input_file):
    try:
        # Detectar o encoding do arquivo
        with open(input_file, 'rb') as f:
            raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding']
        
        # Abre o arquivo de entrada para leitura e o arquivo de saída para escrita
        arquivo_saida = gerar_nome_saida(input_file)
        with open(input_file, 'r', encoding=encoding) as entrada, open(arquivo_saida, 'w', encoding=encoding) as saida:
            # Variável para armazenar a linha atual sendo processada
            linha_em_processo = ''

            # Lê cada linha do arquivo de entrada
            for linha in entrada:
                # 1. Remove espaços em branco no início e no final da linha
                linha = linha.strip()

                # 2. Concatena a linha atual com a linha em processamento
                linha_em_processo += linha

                # 3. Verifica se a linha em processamento está completa (tem todos os campos esperados)
                # Aqui, assumimos que uma linha completa deve ter pelo menos 25 campos (26 colunas)
                if linha_em_processo.count('<>') >= 25:  # Verifica se há pelo menos 25 separadores "<>"
                    # 4. Remove caracteres não imprimíveis da linha
                    linha_em_processo = get_only_characters(linha_em_processo)

                    # 5. Substitui as aspas duplas existentes por espaço em branco
                    linha_em_processo = linha_em_processo.replace('"', ' ')

                    # 6. Divide a linha usando "<>" como delimitador
                    campos = linha_em_processo.split('<>')

                    # 7. Remove espaços em branco do campo do CNPJ (campo 6, índice 5)
                    if len(campos) > 5:  # Verifica se o campo do CNPJ existe
                        campos[5] = campos[5].replace(' ', '')  # Remove espaços do CNPJ

                    # 8. Coloca cada campo entre aspas duplas
                    campos_com_aspas = [f'"{campo.strip()}"' if campo.strip() != '' else '""' for campo in campos]

                    # 9. Junta os campos com ";"
                    linha_formatada = ';'.join(campos_com_aspas)

                    # 10. Escreve a linha formatada no arquivo de saída
                    saida.write(linha_formatada + '\n')

                    # 11. Reinicia a linha em processamento
                    linha_em_processo = ''
                else:
                    # Se a linha não estiver completa, continua concatenando
                    continue

        print(f"Arquivo processado e salvo como: {arquivo_saida}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Exemplo de uso
if __name__ == "__main__":
    input_file = 'NOVO_NATA.csv'  # Substitua pelo caminho do seu arquivo
    process_csv(input_file)