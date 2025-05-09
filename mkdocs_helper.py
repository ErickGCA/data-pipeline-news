"""
Script auxiliar para executar o MkDocs com o pacote instalado.
"""
import os
import sys
import subprocess

def main():
    # Instalar o pacote em modo de desenvolvimento
    subprocess.run(["pip", "install", "-e", "."], check=True)
    
    # Executar o MkDocs
    subprocess.run(["mkdocs", "serve"], check=True)

if __name__ == "__main__":
    main() 