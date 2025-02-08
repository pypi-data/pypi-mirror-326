from setuptools import setup, find_packages

setup(
    name="rpa-arc",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rpa-arc=rpa_arc.cli:main',
        ],
    },
     install_requires=[
        'colorama',
    ],
    author="Luis Costa",
    description="Ferramenta CLI para criar a estrutura de projetos RPA",
    long_description="""
        rpa-arc é uma ferramenta de linha de comando (CLI) projetada para criar rapidamente a estrutura básica de um projeto RPA (Robotic Process Automation).
        Através de um simples comando, o rpa-arc configura todos os diretórios e arquivos essenciais para que você possa começar a desenvolver automações de forma rápida e eficiente.

        A ferramenta gera a seguinte estrutura de diretórios e arquivos:

        /{nome_do_projeto}/
        ├── /src/                # Código-fonte principal
        │   ├── /bots/           # Scripts de automação individuais
        │   ├── /core/           # Módulos reutilizáveis (logs, exceções, autenticação)
        │   ├── /integracoes/    # Conexões com APIs e bancos de dados
        │   ├── /utils/          # Funções auxiliares comuns (manipulação de arquivos, datas)
        │   ├── /api/            # Implementação de APIs para consumo externo
        ├── /config/             # Arquivos de configuração (.env, YAML, JSON)
        ├── /dados/              # Entrada/Saída de arquivos (XML, Excel, PDFs)
        ├── /logs/               # Logs detalhados de execução
        ├── /tests/              # Testes unitários
        ├── requirements.txt     # Dependências do projeto
        ├── README.md            # Documentação do projeto
        └── main.py              # Ponto de entrada do projeto

        Além disso, a ferramenta também inicializa um repositório Git no diretório do projeto e gera um arquivo .gitignore padrão para evitar a inclusão de arquivos desnecessários no controle de versão.

        O objetivo do rpa-arc é proporcionar um início rápido e organizado para novos projetos de automação RPA, permitindo que você se concentre no desenvolvimento das automações em vez de configurar a estrutura do projeto manualmente.
        """,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)