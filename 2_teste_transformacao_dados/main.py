import subprocess
import sys

# Função para instalar pacotes do requirements.txt
def install_requirements():
    try:
        # Executar comando para instalar pacotes do requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        stdout=subprocess.DEVNULL)
        print("Pacotes instalados com sucesso!")
    except Exception as e:
        print(f"Erro ao instalar pacotes: {e}")

# Instalar pacotes antes de executar o resto do código
install_requirements()

def main():
    import pandas as pd
    import pdfplumber, os, zipfile

    file_name = "Anexo_1.pdf"
    save_name = "/tabela_extraida.csv"
    relative_file_path = f"./1_teste_web_scraping/{file_name}"
    relative_save_path = f"./2_teste_transformacao_dados"
    abs_file_path = os.path.abspath(relative_file_path)
    abs_save_path = os.path.abspath(relative_save_path)

    if os.path.exists(abs_file_path):
        print(f"Arquivo {file_name} encontrado na pasta: {abs_file_path}")

        with pdfplumber.open(abs_file_path) as pdf:
            all_tables = []

        # Iterar por todas as páginas do PDF
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                
                # Se houver tabelas na página, processá-las
                for table in tables:
                    df = pd.DataFrame(table)  # Converte para DataFrame do Pandas
                    df.columns = df.iloc[0]  # Define a primeira linha como cabeçalho
                    df = df[1:].reset_index(drop=True)  # Remove a linha duplicada do cabeçalho
                    all_tables.append(df)  # Adiciona ao conjunto de tabelas extraídas
                    
                    print(f"\rExtraíndo tabela da página {page_num}...",end="")
            print(f"\nExtração completa!\n")

        df_final = pd.concat(all_tables, ignore_index=True)
        df_final.columns = [*df_final.columns[:3],"Seg. Odontológia","Seg. Ambulatórial",*df_final.columns[5:]]

        df_final.to_csv(f"{abs_save_path+save_name}", index=False, encoding = "utf-8")
        print(f"Tabela salva como 'tabela_extraida.csv' na pasta {abs_save_path}.")
    else:
        print(f"Arquivo {file_name} não encontrado na pasta {os.getcwd()}")


    def compactar(caminho_do_zip, arquivos_para_compactar):
        with zipfile.ZipFile(caminho_do_zip,"w") as zipf:
            for arquivo in arquivos_para_compactar:
                zipf.write(arquivo, os.path.basename(arquivo))
        print(f"Arquivo compactado na pasta {caminho_do_zip}")

    arquivos = [f"{abs_save_path+save_name}"]
    compactar(f"{abs_save_path}/Teste_{{Amir}}.zip", arquivos)
if __name__ == "__main__":
    main()