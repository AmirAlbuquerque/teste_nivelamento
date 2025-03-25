import requests, zipfile, os

url_anexo1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
url_anexo2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
i = 1
curr_dir = os.getcwd()
project_dir = f"{curr_dir}/1_teste_web_scraping/"
while i != 3:
    if i == 1:
        url = url_anexo1
    elif i== 2:
        url = url_anexo2
    # Obtendo request
    print("Aguardando servidor ...")
    response = requests.get(url)
    #Salvando PDF
    if response.status_code == 200:
        with open(f"{project_dir}Anexo_{i}.pdf","wb") as file:
            file.write(response.content)
        print("PDF salvo com sucesso!")
    else:
        print(f"Falha ao baixar o PDF. Status code: {response.status_code}")
    i += 1

def compactar(caminho_do_zip, arquivos_para_compactar):
    with zipfile.ZipFile(caminho_do_zip,"w") as zipf:
        for arquivo in arquivos_para_compactar:
            zipf.write(arquivo, os.path.basename(arquivo))
    print(f"Arquivo compactados em {caminho_do_zip}")

arquivos = [f"{project_dir}Anexo_1.pdf", f"{project_dir}Anexo_2.pdf"]
compactar(f"{project_dir}Anexos.zip", arquivos)
