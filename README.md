# Lançador Automático de XML

Aplicação para automação de leitura, interpretação de ficheiros XML e integração dos dados processados via API/Sistemas para o Sistema RODOPAR.

## Tecnologias Utilizadas

- **Python 3.x**
- **PyQt / PySide**
- **Módulos XML & API**

## Estrutura do Projeto

- `main.py`: Ponto de entrada do sistema.
- `program.py` / `program_ui.py`: Lógica de parsing do XML e controlo dos eventos de interface.
- `api.py`: Integração com os endpoints dos sistemas de destino.
- `tela.py`: Definição de componentes visuais.

## Como Executar

1. Instale as dependências do projeto:
   ```bash
   pip install PyQt5 requests xmltodict
2. Execute o programa:
   ```bash
   python main.py
