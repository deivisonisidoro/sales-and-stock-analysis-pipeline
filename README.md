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

Após a execução do pipeline, será criada uma pasta chamada `graphs` no diretório principal do projeto. Essa pasta conterá os gráficos gerados com as análises dos dados, como vendas por região, velocidade de vendas e outros insights.

## Testes

### Testes Unitários

Os testes unitários estão localizados na pasta `tests/unit`. Para executá-los, use o comando:

```bash
poetry run pytest tests/unit
```

Esses testes verificam o funcionamento individual de componentes isolados do sistema.

### Testes de Integração

Os testes de integração estão localizados na pasta `tests/integration`. Esses testes verificam como os componentes funcionam juntos. Antes de rodar os testes de integração, você precisa configurar o banco de dados de teste:

1. **Inicie o banco de dados de teste com Docker Compose:**

```bash
docker-compose up -d
```

2. **Crie e configure o arquivo `.env` para os testes de integração, com base no arquivo `.env.example`. Certifique-se de preencher todas as informações necessárias.**

3. **Execute os testes de integração:**

```bash
poetry run pytest tests/integration
```

### Executar Todos os Testes

Para rodar todos os testes (unitários e de integração), use:

```bash
poetry run pytest
```