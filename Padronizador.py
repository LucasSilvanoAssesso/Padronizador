import os
import time
import sys

def get_only_characters(texts):
    if texts is None:
        return ""
    if not isinstance(texts, str):
        texts = str(texts)
    
    return ''.join(char for char in texts if 32 <= ord(char) <= 126)  # Apenas caracteres ASCII imprimíveis

def gerar_nome_saida(input_file):
    base, ext = os.path.splitext(input_file)
    return f"{base}_Tratado{ext}"

def detectar_encoding(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            f.readline()
        return 'utf-8'
    except UnicodeDecodeError:
        return 'latin-1'  # Alternativa comum caso UTF-8 falhe

def process_csv(input_file, option):
    try:
        start_time = time.time()
        encoding = detectar_encoding(input_file)
        arquivo_saida = gerar_nome_saida(input_file)
        
        with open(input_file, 'r', encoding=encoding) as entrada, open(arquivo_saida, 'w', encoding=encoding) as saida:
            linha_contador = 0
            
            for linha in entrada:
                linha = linha.strip()
                if linha.count('<>') < 25:
                    continue  # Pula linhas que não têm o número mínimo esperado de colunas
                
                linha = get_only_characters(linha).replace('"', ' ')
                campos = linha.split('<>')
                
                if len(campos) > 5:
                    campos[5] = campos[5].replace(' ', '')
                
                # Remove espaços extras de valores numéricos
                campos = [campo if not campo.replace(" ", "").isdigit() else campo.replace(" ", "") for campo in campos]
                
                # Insere uma coluna vazia caso a opção seja "1"
                if option == "1":
                    campos.insert(2, "")

                # Formata a linha com aspas e separador ";"
                linha_formatada = ';'.join(f'"{campo.strip()}"' if campo.strip() else '""' for campo in campos)
                saida.write(linha_formatada + '\n')

                linha_contador += 1
        
        end_time = time.time()
        print(f"Arquivo processado e salvo como: {arquivo_saida}")
        print(f"Número total de linhas processadas: {linha_contador}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 xxx.py <nome_do_arquivo_a_ser_tratado> <opção 0 ou 1>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    option = sys.argv[2]
    
    if option not in ["0", "1"]:
        print("Erro: O segundo parâmetro deve ser 0 ou 1.")
        sys.exit(1)
    
    process_csv(input_file, option)
