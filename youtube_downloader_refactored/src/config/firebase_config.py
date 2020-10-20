"""
Módulo de configuração do Firebase.

Este módulo centraliza as configurações do Firebase e fornece
uma interface para autenticação.
"""

import pyrebase
from typing import Dict, Any


class FirebaseConfig:
    """Gerencia a configuração e inicialização do Firebase."""

    _CONFIG: Dict[str, str] = {
        "apiKey": "AIzaSyDneRY8_Zpez6H_izJ2p8oz6fyStECNz2c",
        "authDomain": "gamerdl.firebaseapp.com",
        "projectId": "gamerdl",
        "storageBucket": "gamerdl.firebasestorage.app",
        "messagingSenderId": "237635781428",
        "appId": "1:237635781428:web:ec6526558f92860e775b61",
        "databaseURL": ""
    }

    def __init__(self):
        """Inicializa a conexão com o Firebase."""
        self._firebase = pyrebase.initialize_app(self._CONFIG)
        self._auth = self._firebase.auth()

    @property
    def auth(self) -> Any:
        """Retorna a instância de autenticação do Firebase."""
        return self._auth


# Instância singleton para uso global
firebase_config = FirebaseConfig()
