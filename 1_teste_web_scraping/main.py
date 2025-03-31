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
            print(f"\rErro ao instalar bibliotecas. Arquivo requirements.txt não foi encontrado")
            return False

def main():
    import requests, zipfile, os

    url_anexo1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    url_anexo2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
    i = 1
    curr_dir = os.getcwd()
    project_dir = f"{curr_dir}/1_teste_web_scraping/"
    if not os.path.isdir(project_dir):
        project_dir=f"{curr_dir}/"
    
    while i != 3:
        if i == 1:
            url = url_anexo1
        elif i== 2:
            url = url_anexo2
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event, f"Baixando Anexo {i}..."))
        loading_thread.start()
        # Obtendo request
        # print("Aguardando servidor ...")
        response = requests.get(url)
        stop_event.set()
        loading_thread.join()
        #Salvando PDF
        if response.status_code == 200:
            with open(f"{project_dir}Anexo_{i}.pdf","wb") as file:
                file.write(response.content)
            print(f"\rAnexo_{i} salvo com sucesso!")
        else:
            print(f"\rFalha ao baixar o PDF. Status code: {response.status_code}")
        i += 1

    def compactar(caminho_do_zip, arquivos_para_compactar):
        with zipfile.ZipFile(caminho_do_zip,"w") as zipf:
            for arquivo in arquivos_para_compactar:
                zipf.write(arquivo, os.path.basename(arquivo))
        print(f"\nArquivo compactados em {caminho_do_zip}")

    arquivos = [f"{project_dir}Anexo_1.pdf", f"{project_dir}Anexo_2.pdf"]
    compactar(f"{project_dir}Anexos.zip", arquivos)

# Instalar bibliotecas antes de executar o resto do código
if install_requirements():
    main()