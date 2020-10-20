# Arquitetura do Projeto

## Visão Geral

Este projeto segue uma arquitetura em camadas, separando responsabilidades e facilitando manutenção e testes.

## Camadas da Aplicação

### 1. Camada de Apresentação (UI)
**Localização:** `src/ui/`

Responsável pela interface gráfica e interação com o usuário.

- **login_window.py**: Janela de autenticação
- **downloader_window.py**: Janela principal de download
- **base_components.py**: Componentes reutilizáveis de UI
- **download_thread.py**: Thread para download em background

**Princípios aplicados:**
- Separação de responsabilidades (UI não contém lógica de negócio)
- Componentes reutilizáveis (DRY)
- Injeção de dependências via callbacks

### 2. Camada de Serviços (Services)
**Localização:** `src/services/`

Contém a lógica de negócio da aplicação.

- **auth_service.py**: Gerencia autenticação de usuários
- **download_service.py**: Gerencia download de vídeos
- **video_info_service.py**: Obtém informações de vídeos

**Princípios aplicados:**
- Single Responsibility Principle (cada serviço tem uma responsabilidade)
- Dependency Inversion (depende de abstrações, não implementações)
- Facilita testes unitários com mocks

### 3. Camada de Modelos (Models)
**Localização:** `src/models/`

Define estruturas de dados e exceções personalizadas.

- **video_info.py**: Dataclasses para informações de vídeo
- **exceptions.py**: Exceções personalizadas

**Princípios aplicados:**
- Encapsulamento de dados
- Type hints para clareza
- Métodos auxiliares nos modelos

### 4. Camada de Configuração (Config)
**Localização:** `src/config/`

Centraliza configurações e constantes.

- **firebase_config.py**: Configuração do Firebase
- **constants.py**: Constantes e estilos da aplicação

**Princípios aplicados:**
- Centralização de configurações
- Facilita manutenção
- Evita magic numbers e strings

### 5. Camada de Utilitários (Utils)
**Localização:** `src/utils/`

Funções auxiliares reutilizáveis.

- **validators.py**: Validadores de dados
- **system_utils.py**: Utilitários de sistema

**Princípios aplicados:**
- Funções puras quando possível
- Reutilização de código
- Facilita testes

## Fluxo de Dados

```
User Input → UI Layer → Services Layer → External APIs/Libraries
                ↓           ↓
            Models      Config/Utils
```

## Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
Cada classe tem uma única responsabilidade:
- `AuthService`: apenas autenticação
- `DownloadService`: apenas download
- `VideoInfoService`: apenas informações de vídeo

### Open/Closed Principle (OCP)
Classes abertas para extensão, fechadas para modificação:
- Novos formatos de download podem ser adicionados sem modificar `DownloadService`
- Novos validadores podem ser criados sem modificar existentes

### Liskov Substitution Principle (LSP)
Componentes de UI herdam de classes base do PyQt5 corretamente.

### Interface Segregation Principle (ISP)
Interfaces específicas e coesas:
- Callbacks específicos para cada necessidade
- Serviços com métodos focados

### Dependency Inversion Principle (DIP)
Dependências de abstrações:
- UI depende de serviços via interfaces
- Serviços podem ser mockados para testes

## Padrões de Design Utilizados

### Singleton
- `FirebaseConfig`: instância única de configuração

### Observer
- Signals e slots do PyQt5 para comunicação entre componentes

### Strategy
- Diferentes estratégias de download (qualidade, formato)

### Factory
- Criação de componentes de UI via métodos factory

## Testabilidade

A arquitetura facilita testes unitários:
- Serviços podem ser testados isoladamente
- Mocks podem substituir dependências externas
- Validadores têm testes de casos extremos
- Cobertura de código > 80%

## Extensibilidade

Para adicionar novas funcionalidades:

1. **Novo formato de download**: Adicionar em `DownloadFormats`
2. **Nova autenticação**: Criar novo serviço implementando interface similar
3. **Nova validação**: Adicionar classe em `validators.py`
4. **Nova UI**: Criar componente herdando de `base_components.py`

## Dependências Externas

- **PyQt5**: Framework de UI
- **yt-dlp**: Download de vídeos
- **Pyrebase4**: Integração com Firebase
- **requests**: Requisições HTTP
- **pytest**: Framework de testes
