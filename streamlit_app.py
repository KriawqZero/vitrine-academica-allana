import sys
import os

# Adicionar o diretório pages ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

# Importar e executar a função principal do login
from login import main

if __name__ == "__main__":
    main() 