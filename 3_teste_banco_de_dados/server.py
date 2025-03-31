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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_server.txt"],
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
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements_server.txt"],
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
            print(f"\rErro ao instalar bibliotecas. Arquivo requirements_server.txt não foi encontrado")
            return False

def main():
    import psycopg2, os
    from dotenv import load_dotenv
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # Definir parâmetros de conexão
    db_config = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": "5432",
        "sslmode": "require"
    }

    # Configurando os paths
    file_name = "main.sql"
    relative_file_path = f"./3_teste_banco_de_dados/{file_name}"
    absolute_file_path = os.path.abspath(relative_file_path)
    print(absolute_file_path)

    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False
        cursor = conn.cursor()

        # Executar uma consulta simples
        cursor.execute("SELECT NOW();")  # Obtém a data e hora do servidor
        result = cursor.fetchone()
        print("Conexão bem-sucedida! Hora do servidor:", result)

        # Abrir e ler arquivo SQL
        print(f"Executando arquivo SQL: {absolute_file_path}")
        with open(absolute_file_path,'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Executar sql
        cursor.execute(sql_script)
        conn.commit()
        print("Script SQL executado com sucesso!")

        # Fechar conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro ao conectar:", e)

# Instalar bibliotecas antes de executar o resto do código
if install_requirements():
    main()