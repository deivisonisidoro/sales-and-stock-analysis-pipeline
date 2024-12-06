# Pipeline de Análise de Vendas e Estoque

Este projeto implementa um pipeline de ETL (Extração, Transformação e Carga) para analisar dados de vendas e estoque. O pipeline extrai dados de diferentes fontes, aplica transformações como limpeza de dados e cálculo de métricas, carrega os dados no banco de dados e gera visualizações de vendas por região e velocidade de vendas.

## Tecnologias Utilizadas

- **Python 3.x**
- **Poetry**: Gerenciamento de dependências e ambientes virtuais.
- **Pandas**: Para manipulação de dados.
- **Matplotlib** e **Seaborn**: Para visualização de dados.
- **PostgreSQL**: Banco de dados para armazenar dados processados.

## Requisitos

- Python 3.10 ou superior
- Poetry para gerenciamento de dependências
- Docker e Docker Compose (para rodar o banco de dados PostgreSQL)

## Como Rodar o Projeto

### 1. Clonar o Repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone https://github.com/SEU_USUARIO/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar o Arquivo `.env`

Antes de rodar a aplicação, crie o arquivo `.env` com base no arquivo `.env.example` que se encontra no repositório. Isso é necessário para definir as variáveis de ambiente para a conexão com o banco de dados e outras configurações:

```bash
cp .env.example .env
```

### 3. Criar o Ambiente Virtual

Instale o Poetry (se ainda não o tiver instalado):

- **No Linux/macOS:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- **No Windows:**

Baixe o instalador [aqui](https://python-poetry.org/docs/#installation).

### 4. Instalar as Dependências

Instale as dependências do projeto usando o Poetry:

```bash
poetry install
```

### 5. Rodar o Banco de Dados com Docker Compose

O banco de dados PostgreSQL está configurado para rodar com Docker Compose. Para rodar o banco de dados, siga os passos abaixo:

1. Certifique-se de ter o Docker e o Docker Compose instalados.
2. Execute o seguinte comando para iniciar o banco de dados PostgreSQL:

```bash
docker-compose up -d
```

Isso vai levantar um container com o PostgreSQL rodando na porta `5433` (configurado no `docker-compose.yml`), com as credenciais definidas em `.env` ou nas variáveis de ambiente do arquivo `docker-compose.yml`.

### 6. Rodar o Pipeline

Para rodar o pipeline, execute o seguinte comando:

```bash
poetry run python run.py
```

Isso vai executar o pipeline completo: extração dos dados, transformação, carga no banco de dados e visualização dos resultados.

### 7. Executar os Testes

Para rodar os testes, você pode usar o seguinte comando:

```bash
poetry run pytest
```

## Estrutura do Projeto

A estrutura do projeto segue o padrão de um pipeline de dados, com as seguintes pastas e arquivos principais:

```
├── src/
│   ├── analysis/
│   │   ├── visualize.py          # Visualização de dados de vendas
│   ├── driver/
│   │   ├── dataloader.py        # Carregamento dos dados
│   ├── stages/
│   │   ├── extract/
│   │   │   ├── extract_data.py  # Extração de dados
│   │   ├── load/
│   │   │   ├── load_data.py     # Carga de dados no banco
│   │   ├── transform/
│   │   │   ├── data_cleaner.py  # Limpeza dos dados
│   │   │   ├── sales_transform.py # Transformações de vendas
│   │   │   ├── stock_transformer.py # Transformações de estoque
│   ├── infra/
│   │   ├── database_connector.py # Conexão com o banco de dados
│   │   ├── database_repository.py # Repositório de dados
│   ├── errors/
│   │   ├── extract_error.py      # Erros relacionados à extração
│   │   ├── load_error.py         # Erros relacionados à carga
│   │   ├── transform_error.py    # Erros relacionados à transformação
│   ├── config/
│   │   ├── settings.py           # Configurações do projeto
│   ├── main_pipeline.py          # Arquivo principal para rodar o pipeline
└── docker-compose.yml            # Configuração do Docker Compose para o banco de dados
└── pyproject.toml               # Configuração do Poetry
└── .env                         # Arquivo de variáveis de ambiente
```