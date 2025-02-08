import os
import argparse
import shutil
import re

from colorama import init, Fore, Style

init(autoreset=True)

# Estrutura do projeto
ESTRUTURA = {
    "src": ["bots", "core", "integracoes", "utils", "api"],
    "config": [],
    "dados": [],
    "logs": [],
    "tests": [],
}

ARQUIVOS_BASE = [
    "requirements.txt",
    "README.md",
    "main.py"
]

def validar_nome_projeto(nome):
    """Verifica se o nome do projeto é válido (sem espaços e caracteres especiais)."""
    if re.match(r'^[a-zA-Z0-9_-]+$', nome):
        return True
    print("Erro: O nome do projeto contém caracteres inválidos! Use apenas letras, números, hífens ou underscores.")
    return False

def criar_arquitetura(nome_projeto):
    caminho_base = os.path.join(os.getcwd(), nome_projeto)

    if os.path.exists(caminho_base):
        print(f"Erro: O diretório '{nome_projeto}' já existe!")
        return

    if not validar_nome_projeto(nome_projeto):
        return

    os.makedirs(caminho_base)

    # Criar diretórios
    for pasta, subpastas in ESTRUTURA.items():
        pasta_path = os.path.join(caminho_base, pasta)
        os.makedirs(pasta_path, exist_ok=True)
        for subpasta in subpastas:
            os.makedirs(os.path.join(pasta_path, subpasta), exist_ok=True)

    # Criar arquivos base
    for arquivo in ARQUIVOS_BASE:
        caminho_arquivo = os.path.join(caminho_base, arquivo)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            if arquivo == "README.md":
                f.write(f"# {nome_projeto}\n\nDescrição do projeto.")
                f.write("\n\n## Arquitetura do Projeto")
                f.write("\nEsta ferramenta cria uma estrutura básica de um projeto RPA com a seguinte organização:")
                f.write("\n\n```\n/projeto_rpa/")
                f.write("\n│── /src/                # Código-fonte principal")
                f.write("\n│   ├── /bots/           # Scripts de automação individuais")
                f.write("\n│   ├── /core/           # Módulos reutilizáveis (logs, exceções, autenticação)")
                f.write("\n│   ├── /integracoes/    # Conexões com APIs e bancos de dados")
                f.write("\n│   ├── /utils/          # Funções auxiliares comuns (manipulação de arquivos, datas)")
                f.write("\n│   ├── /api/            # Implementação de APIs para consumo externo")
                f.write("\n│── /config/             # Arquivos de configuração (.env, YAML, JSON)")
                f.write("\n│── /dados/              # Entrada/Saída de arquivos (XML, Excel, PDFs)")
                f.write("\n│── /logs/               # Logs detalhados de execução")
                f.write("\n│── /tests/              # Testes unitários")
                f.write("\n│── requirements.txt     # Dependências do projeto")
                f.write("\n│── README.md            # Documentação")
                f.write("\n│── main.py              # Ponto de entrada do projeto")
                f.write("\n```\n")
            elif arquivo == "requirements.txt":
                f.write("# Lista de dependências do projeto\n")
            elif arquivo == "main.py":
                f.write("# Ponto de entrada do projeto\n\nif __name__ == '__main__':\n    print('Projeto iniciado!')")

    inicializar_git(caminho_base)

    print(Fore.GREEN + f"✅ Projeto '{nome_projeto}' foi criado com sucesso! 🎉\n")
    print(Fore.YELLOW + f"🔧 Estrutura do projeto foi configurada corretamente com os seguintes diretórios e arquivos:")
    print(Fore.CYAN + f"└── {nome_projeto}/")
    print(Fore.CYAN + f"    ├── /src/                # Código-fonte principal")
    print(Fore.CYAN + f"    ├── /config/             # Arquivos de configuração")
    print(Fore.CYAN + f"    ├── /dados/              # Entrada/Saída de arquivos")
    print(Fore.CYAN + f"    ├── /logs/               # Logs detalhados de execução")
    print(Fore.CYAN + f"    ├── /tests/              # Testes unitários")
    print(Fore.CYAN + f"    ├── requirements.txt     # Dependências do projeto")
    print(Fore.CYAN + f"    ├── README.md            # Documentação do projeto")
    print(Fore.CYAN + f"    └── main.py              # Ponto de entrada do projeto\n")
    print(Fore.GREEN + f"🚀 Agora você pode começar a desenvolver seu Robo 🤖!\n")

def inicializar_git(caminho_base):
    """Inicializa um repositório Git no diretório do projeto e cria um .gitignore padrão."""
    os.system(f"cd {caminho_base} && git init")
    with open(os.path.join(caminho_base, ".gitignore"), "w") as f:
        f.write("""
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.env
logs/
""")

def main():
    parser = argparse.ArgumentParser(description="Ferramenta para criar estrutura de projetos RPA.")
    parser.add_argument("nome", help="Nome do projeto")
    args = parser.parse_args()
    criar_arquitetura(args.nome)

if __name__ == "__main__":
    main()