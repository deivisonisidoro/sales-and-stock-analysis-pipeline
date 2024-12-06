## Processos Desenvolvidos e Soluções Encontradas

### 1. **Extração de Dados (Extract Data)**

**Processo Desenvolvido:**
A primeira etapa do pipeline é a extração de dados. Para isso, desenvolvemos o módulo `ExtractData` que interage com o `DataLoader`. O objetivo é extrair dados de fontes diversas, como bancos de dados ou APIs externas, de maneira eficiente e estruturada. O `DataLoader` é uma classe responsável por carregar e fornecer os dados necessários para as transformações subsequentes.

**Solução Encontrada:**
Uma das principais dificuldades ao lidar com a extração de dados foi garantir que os dados estivessem no formato adequado para as etapas de transformação. Utilizamos um contrato de extração para organizar a estrutura dos dados, com validações específicas que garantem que os dados sejam consistentes antes de passar para a próxima fase.

### 2. **Transformação de Dados (Data Transformation)**

**Processo Desenvolvido:**
Após a extração, os dados passam pela etapa de transformação, que é composta por várias subetapas:

- **Limpeza de Dados (Data Cleaner)**: A classe `DataCleaner` foi desenvolvida para lidar com dados sujos e inconsistentes, removendo valores nulos, duplicados ou errôneos. Essa etapa é crucial para garantir a qualidade dos dados antes de qualquer análise ou agregação.
  
- **Transformação de Vendas (Sales Transformer)**: A transformação de vendas envolve cálculos de métricas como a velocidade de vendas, que considera o volume de vendas em um período de tempo. A classe `SalesTransformer` é responsável por calcular esses indicadores de forma eficiente.

- **Transformação de Estoque (Stock Transformer)**: A classe `StockTransformer` calcula o estoque disponível, considerando entradas e saídas de produtos. Esse cálculo é necessário para entender a relação entre o estoque e as vendas realizadas, e assim otimizar o planejamento de compras.

**Solução Encontrada:**
Durante a transformação de dados, uma das dificuldades enfrentadas foi a necessidade de sincronizar informações entre as diferentes fontes de dados (vendas, estoque e lojas). Para isso, utilizamos uma abordagem baseada em contratos de dados bem definidos, que permite mapear e integrar dados de diferentes origens de maneira uniforme. Além disso, foi necessário garantir que os cálculos de métricas, como a velocidade de vendas e estoque disponível, fossem feitos de maneira eficiente para suportar grandes volumes de dados.

### 3. **Carga de Dados (Load Data)**

**Processo Desenvolvido:**
Na etapa de carga, os dados transformados são inseridos no banco de dados PostgreSQL. A classe `LoadData` é responsável por interagir com o repositório de dados para inserir informações nas tabelas adequadas. Para otimizar a inserção, usamos a técnica de *bulk insert*, que permite carregar grandes volumes de dados de uma só vez, minimizando o impacto no desempenho.

**Solução Encontrada:**
Uma das maiores dificuldades foi garantir que a inserção de dados fosse realizada de forma eficiente, especialmente em cenários com grandes volumes de dados. Para isso, utilizamos a função `execute_values` do PostgreSQL, que permite inserir múltiplos registros em uma única transação, aumentando significativamente a performance. Além disso, implementamos um mecanismo de tratamento de erros, de modo que qualquer falha na carga de dados seja corretamente registrada e o processo seja revertido, evitando inconsistências no banco de dados.

### 4. **Análise de Dados (Analyze Data)**

**Processo Desenvolvido:**
Após a carga dos dados no banco de dados, a análise de dados começa com o cálculo de métricas e indicadores importantes. A classe `SalesByRegionAnalyzer` realiza uma análise de vendas por região, proporcionando uma visão detalhada de como as vendas variam de acordo com a localização das lojas. Essa análise permite identificar padrões e tendências que podem ajudar a direcionar estratégias de vendas e estoque.

**Solução Encontrada:**
Durante a análise de dados, encontramos a necessidade de segmentar as vendas por regiões de forma eficiente. Para isso, utilizamos um modelo de dados bem estruturado, que inclui informações sobre as lojas e as regiões a que pertencem. Esse modelo foi essencial para garantir que a análise fosse realizada de forma precisa, levando em consideração todas as variáveis relevantes para cada região.

### 5. **Visualização de Dados (Data Visualization)**

**Processo Desenvolvido:**
A última etapa do pipeline envolve a visualização dos resultados das análises. A classe `SalesVisualizer` foi responsável por gerar gráficos e plots que ilustram as métricas calculadas, como vendas por região, velocidade de vendas e desempenho por grupo de produtos. As visualizações são feitas com o uso das bibliotecas `Matplotlib` e `Seaborn`, que proporcionam gráficos claros e informativos.

**Solução Encontrada:**
Uma das dificuldades foi garantir que os gráficos fossem informativos e fáceis de interpretar. Para isso, seguimos boas práticas de visualização de dados, como a escolha adequada de tipos de gráficos (barras, linhas, etc.) e a utilização de cores e rótulos claros. Também implementamos uma modularização das visualizações para que diferentes tipos de gráficos possam ser gerados com facilidade, dependendo da análise que se deseja realizar.

### 6. **Uso do Docker para Banco de Dados**

**Processo Desenvolvido:**
Para facilitar a configuração e o gerenciamento do banco de dados PostgreSQL, utilizamos o Docker com o arquivo `docker-compose.yml`. Esse arquivo configura o container do banco de dados e garante que ele seja iniciado de forma consistente em qualquer ambiente.

**Solução Encontrada:**
A principal vantagem do uso do Docker foi a facilidade de configurar o banco de dados sem a necessidade de instalação manual. Isso também permitiu que todos os membros da equipe e ambientes de desenvolvimento utilizassem a mesma configuração de banco de dados, garantindo que os dados fossem acessados de maneira consistente durante todo o processo de desenvolvimento.
