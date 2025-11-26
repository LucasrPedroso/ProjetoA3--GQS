# YouTube Gamer DL - Versão Refatorada

## Descrição

Aplicação desktop para download de vídeos do YouTube com autenticação Firebase, completamente refatorada seguindo princípios de Programação Orientada a Objetos e boas práticas de desenvolvimento.

## Melhorias Implementadas

### Legibilidade
- Nomes de variáveis e funções claros e significativos
- Código organizado em módulos com responsabilidades bem definidas
- Uso de type hints para melhor documentação do código

### Estrutura
- Arquitetura em camadas (UI, Services, Models, Config, Utils)
- Modularização adequada com separação de responsabilidades
- Redução significativa de repetições de código

### Comentários e Documentação
- Docstrings em todos os módulos, classes e métodos
- Comentários explicativos apenas quando necessário
- Documentação clara de parâmetros e retornos

### Boas Práticas

#### Princípios SOLID
- **S**ingle Responsibility Principle: Cada classe tem uma única responsabilidade
- **O**pen/Closed Principle: Classes abertas para extensão, fechadas para modificação
- **L**iskov Substitution Principle: Uso adequado de herança
- **I**nterface Segregation Principle: Interfaces específicas e coesas
- **D**ependency Inversion Principle: Dependências de abstrações, não de implementações

#### Outros Princípios
- **DRY** (Don't Repeat Yourself): Eliminação de código duplicado
- **KISS** (Keep It Simple, Stupid): Soluções simples e diretas
- **YAGNI** (You Aren't Gonna Need It): Implementação apenas do necessário

### Testes
- Testes unitários completos para todas as camadas
- Cobertura de casos de sucesso e erro
- Uso de mocks para isolamento de dependências

## Estrutura do Projeto

```
youtube_downloader_refactored/
├── src/
│   ├── config/              # Configurações e constantes
│   │   ├── firebase_config.py
│   │   └── constants.py
│   ├── models/              # Modelos de dados
│   │   ├── video_info.py
│   │   └── exceptions.py
│   ├── services/            # Lógica de negócio
│   │   ├── auth_service.py
│   │   ├── download_service.py
│   │   └── video_info_service.py
│   ├── ui/                  # Interface gráfica
│   │   ├── base_components.py
│   │   ├── login_window.py
│   │   ├── downloader_window.py
│   │   └── download_thread.py
│   ├── utils/               # Utilitários
│   │   ├── validators.py
│   │   └── system_utils.py
│   └── app_controller.py    # Controlador principal
├── tests/                   # Testes unitários
│   ├── test_auth_service.py
│   ├── test_download_service.py
│   ├── test_video_info_service.py
│   └── test_validators.py
├── main.py                  # Ponto de entrada
└── requirements.txt         # Dependências
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Exporte os cookies do YouTube usando a extensão "Get cookies.txt clean"
4. Salve o arquivo como `youtube.com_cookies.txt` na pasta raiz

## Execução

```bash
python main.py
```

## Execução dos Testes

```bash
pytest tests/ -v
```

## Requisitos

- Python 3.7+
- PyQt5
- yt-dlp
- requests
- Pyrebase4
- FFmpeg (para conversão de vídeos)

## Funcionalidades

- Autenticação de usuários via Firebase
- Download de vídeos em diferentes qualidades
- Download de áudio em MP3
- Visualização de thumbnail e título do vídeo
- Barra de progresso em tempo real
- Interface moderna e responsiva

## Licença

Este projeto é fornecido como exemplo de refatoração e boas práticas de programação.
