import subprocess
import sys
import threading
import time

# Função para animar o carregamento
def loading_animation(stop_event, message):
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        print(f"\r{message} {symbols[i % len(symbols)]}", end="", flush=True)
        time.sleep(0.2)
        i += 1
    print("\r" + " " * len(message) + " ", end="")

# Função para instalar pacotes do requirements.txt
def install_requirements():
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event, "Instalando bibliotecas..."))

    try:
        # Executar comando para instalar pacotes do requirements.txt
        loading_thread.start()
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
        stop_event.set()
        loading_thread.join()
        print("\rBibliotecas instaladas com sucesso!\n")
        time.sleep(5)
        return True
    except subprocess.CalledProcessError:
        try:
            # Executar comando para instalar pacotes do requirements.txt
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
            stop_event.set()
            loading_thread.join()
            print("\rBibliotecas instaladas com sucesso!")
            time.sleep(5)
            return True
        except subprocess.CalledProcessError:
            stop_event.set()
            loading_thread.join()
            print(f"\rErro ao instalar pacotes. Arquivo requirements.txt não foi encontrado")
            return False

def main():
    import pandas as pd
    import pdfplumber, os, zipfile

    file_name = "Anexo_1.pdf"
    save_name = "/tabela_extraida.csv"
    #Caminho import
    relative_file_path = f"./1_teste_web_scraping/{file_name}"
    abs_file_path = os.path.abspath(relative_file_path)
    #Caminho export
    relative_save_path = f"./2_teste_transformacao_dados"
    abs_save_path = os.path.abspath(relative_save_path)

    if not os.path.exists(abs_file_path):
        relative_file_path = f"../1_teste_web_scraping/{file_name}"
        abs_file_path = os.path.abspath(relative_file_path)
        abs_save_path = os.getcwd()

    if os.path.exists(abs_file_path):
        print(f"Arquivo {file_name} encontrado na pasta: {abs_file_path}\n")

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
            print(f"\rExtração completa!                                   \n")

        df_final = pd.concat(all_tables, ignore_index=True)
        df_final.columns = [*df_final.columns[:3],"Seg. Odontológia","Seg. Ambulatórial",*df_final.columns[5:]]

        df_final.to_csv(f"{abs_save_path+save_name}", index=False, encoding = "utf-8")
        print(f"Tabela salva como 'tabela_extraida.csv' na pasta {abs_save_path}.\n")
    else:
        print(f"Arquivo {file_name} não encontrado na pasta {os.getcwd()}\n")


    def compactar(caminho_do_zip, arquivos_para_compactar):
        with zipfile.ZipFile(caminho_do_zip,"w") as zipf:
            for arquivo in arquivos_para_compactar:
                zipf.write(arquivo, os.path.basename(arquivo))
        print(f"Arquivo compactado na pasta {caminho_do_zip}\n")

    arquivos = [f"{abs_save_path+save_name}"]
    compactar(f"{abs_save_path}/Teste_{{Amir}}.zip", arquivos)

# Instalar bibliotecas antes de executar o resto do código
if install_requirements():
    main()