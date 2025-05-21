import subprocess
import platform
import os

def instalar_docker_windows():
    if platform.system() != "Windows":
        print("Este script é para Windows.")
        return

    print("Atualizando WSL...")
    try:
        subprocess.run(['wsl', '--update'], check=True)
        print("WSL atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar WSL: {e}")

    print("Instalando Docker Desktop via winget...")
    try:
        subprocess.run([
            'winget', 'install', '--id', 'Docker.DockerDesktop', '-e',
            '--accept-source-agreements', '--accept-package-agreements'
        ], check=True)
        print("Docker instalado com sucesso.")
    except subprocess.CalledProcessError as e:
        if e.returncode == 2316632107: 
            print("Docker já está instalado. Continuando...")
        else:
            print(f"Erro inesperado na instalação do Docker: {e}")
            return

    print("Iniciando Docker Desktop...")
    caminho = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if os.path.exists(caminho):
        subprocess.Popen([caminho], shell=True)
        print("Docker Desktop iniciado com sucesso.")
    else:
        print("Docker Desktop não encontrado no caminho padrão.")