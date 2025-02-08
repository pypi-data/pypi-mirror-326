rpa-arc
=======

**rpa-arc** é uma ferramenta CLI para criar automaticamente a estrutura de projetos de RPA.

Instalação
----------

Para instalar, use:

.. code-block:: bash

    pip install rpa-arc

Uso
---

Para criar um novo projeto RPA, execute:

.. code-block:: bash

    rpa-arc nome_do_projeto

Isso criará a seguinte estrutura de pastas:

.. code-block:: text

    /nome_do_projeto/
    ├── src/
    │   ├── bots/
    │   ├── core/
    │   ├── integracoes/
    │   ├── utils/
    │   ├── api/
    ├── config/
    ├── dados/
    ├── logs/
    ├── tests/
    ├── requirements.txt
    ├── README.md
    ├── main.py

Recursos
--------

- Gera automaticamente pastas organizadas para o projeto.
- Cria um arquivo `.gitignore` para boas práticas.
- Inclui um `README.md` com explicações sobre a arquitetura.
- Valida o nome do projeto para evitar caracteres inválidos.

Licença
-------

Este projeto está licenciado sob a **MIT License**.