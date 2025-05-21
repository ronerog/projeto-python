import psycopg2
from dotenv import load_dotenv
import os

def criar_conexao():
    load_dotenv()
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
    except psycopg2.Error as erro:
        print("Erro ao conectar:", erro)
        return None