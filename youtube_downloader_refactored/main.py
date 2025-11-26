"""
Ponto de entrada da aplicação YouTube Gamer DL.

Este módulo inicializa e executa a aplicação.
"""

import sys
from src.app_controller import AppController


def main() -> int:
    """
    Função principal da aplicação.
    
    Returns:
        Código de saída da aplicação
    """
    controller = AppController()
    return controller.run()


if __name__ == "__main__":
    sys.exit(main())
