import pandas as pd
import pdfplumber, os

file_name = "Anexo_1.pdf"
relative_file_path = f"../1_teste_web_scraping/{file_name}"
abs_file_path = os.path.abspath(relative_file_path)

if os.path.exists(abs_file_path):
    print(f"Arquivo {file_name} encontrado na pasta: {abs_file_path}")
else:
    print(f"Arquivo {file_name} não encontrado na pasta {os.getcwd()}")