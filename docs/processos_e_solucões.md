## Processos Desenvolvidos e Soluções Encontradas

### 1. **Extração de Dados (Extract Data)**

**Processo Desenvolvido:**  
A primeira etapa do pipeline foi a extração de dados. Para isso, desenvolvi o módulo `ExtractData`, que interage com o `DataLoader`. O objetivo foi extrair dados de fontes diversas, como bancos de dados ou APIs externas, de maneira eficiente e estruturada. O `DataLoader` é uma classe responsável por carregar e fornecer os dados necessários para as transformações subsequentes.

**Solução Encontrada:**  
Uma das principais dificuldades ao lidar com a extração de dados foi garantir que os dados estivessem no formato adequado para as etapas de transformação. Utilizei um contrato de extração para organizar a estrutura dos dados, com validações específicas que garantem que os dados fossem consistentes antes de passar para a próxima fase.

### 2. **Transformação de Dados (Data Transformation)**

**Processo Desenvolvido:**  
Após a extração, os dados passaram pela etapa de transformação, que agora é realizada por uma única classe, `TransformData`. Esta classe coordena várias operações de transformação, como:

- **Limpeza de Dados (Data Cleaning):** Na classe `TransformData`, desenvolvi o método `_clean_data` para lidar com dados sujos e inconsistentes, removendo duplicatas e preenchendo valores ausentes. Essa etapa é crucial para garantir que os dados estejam em um formato adequado antes de qualquer análise ou agregação.

- **Cálculo da Velocidade de Vendas (Sales Velocity Calculation):** Utilizei o método `_calculate_sales_velocity` para calcular a velocidade de vendas, que leva em conta o volume de vendas em relação ao estoque disponível, combinando dados de vendas e estoque para determinar a eficiência das vendas.

- **Cálculo do Estoque Disponível (Available Stock Calculation):** O método `_calculate_available_stock` foi implementado para calcular o estoque disponível subtraindo o estoque em trânsito do estoque total. Esse cálculo é importante para otimizar o planejamento de compras e evitar rupturas de estoque.

- **Cálculo de Vendas por Região (Sales by Region Calculation):** No método `_calculate_sales_by_region`, realizei o agrupamento das vendas por região (estado e cidade), fornecendo uma visão mais detalhada de como as vendas variam geograficamente, o que pode direcionar estratégias específicas para cada local.

**Solução Encontrada:**  
Durante a transformação de dados, uma das dificuldades foi garantir a integração e sincronização das informações provenientes de diferentes fontes de dados (vendas, estoque e lojas). Para isso, utilizei uma abordagem baseada em contratos de dados bem definidos, o que permitiu mapear e integrar dados de diferentes origens de maneira consistente. Além disso, garanti que os cálculos das métricas, como a velocidade de vendas e o estoque disponível, fossem feitos de maneira eficiente, mesmo com grandes volumes de dados.

### 3. **Carga de Dados (Data Loading)**

**Processo Desenvolvido:**  
Após a transformação dos dados, a próxima etapa foi o carregamento para o banco de dados. Para isso, desenvolvi a classe `LoadData`, responsável por carregar os dados transformados nas tabelas apropriadas do banco de dados, utilizando uma interface de repositório para interagir com o banco de dados. Essa classe executa as seguintes operações:

- **Validação dos Dados:** Antes de carregar os dados no banco de dados, a classe `LoadData` valida os DataFrames presentes no contrato de transformação (`TransformContract`). Se algum DataFrame estiver vazio, um erro será gerado, evitando que dados incompletos sejam carregados.

- **Criação das Tabelas:** Caso as tabelas necessárias não existam, a classe `LoadData` verifica a existência das tabelas no banco de dados, e se necessário, cria-as utilizando consultas SQL armazenadas na pasta `src/queries/create`. Isso garante que a estrutura do banco de dados esteja configurada antes da inserção dos dados.

- **Inserção de Dados:** Com as tabelas validadas ou criadas, os dados transformados são inseridos nas tabelas do banco de dados. Cada campo do contrato de transformação é percorrido, e se for um DataFrame, os dados são inseridos na tabela correspondente.

**Solução Encontrada:**  
Durante o processo de carga, uma das principais dificuldades foi garantir que as tabelas estivessem corretamente configuradas antes da inserção dos dados e que a integridade dos dados fosse mantida ao longo do processo. Para resolver isso, implementei a verificação e criação das tabelas de forma automatizada e a validação dos dados para garantir que dados incompletos não fossem inseridos no banco de dados. Além disso, a abordagem baseada em contratos de dados bem definidos permite que os dados sejam carregados de forma eficiente e estruturada.

### 4. **Análise de Dados (Data Analysis)**

**Processo Desenvolvido:**  
Após a carga dos dados, a próxima etapa no fluxo de dados foi a análise, que visa gerar relatórios e insights valiosos para os tomadores de decisão. A classe `AnalyzeData` foi desenvolvida para realizar as análises de vendas e acionar a visualização desses dados. A classe realiza as seguintes tarefas:

- **Execução da Análise:** O método `execute_analysis` é responsável por executar a análise dos dados. Ele busca as consultas SQL necessárias para a análise dos dados de vendas (como vendas por produto, por filial, e outras métricas) de arquivos armazenados na pasta `src/queries/analysis`. As consultas SQL são lidas a partir desses arquivos e executadas através do repositório de banco de dados, recuperando as informações necessárias.

- **Verificação de Consultas:** Antes de proceder, o método verifica se todas as consultas SQL foram encontradas e carregadas corretamente. Caso alguma consulta esteja ausente, um erro é informado.

- **Execução das Consultas e Criação do Contrato de Análise:** As consultas SQL carregadas são executadas para buscar os dados necessários para a análise. Em seguida, um contrato de análise (`AnalyzeContract`) é criado com esses dados, organizando-os de forma estruturada para ser consumido pela camada de visualização.

- **Geração de Relatórios:** O contrato de análise é passado para o visualizador responsável pela geração de relatórios e gráficos, que proporcionam uma visão mais clara e prática dos dados de vendas analisados.

**Solução Encontrada:**  
A principal dificuldade encontrada foi garantir que as consultas SQL estivessem corretamente configuradas e que os dados de vendas fossem analisados de maneira eficiente e sem falhas. Para superar isso, desenvolvi uma abordagem em que as consultas são lidas de arquivos específicos, facilitando a manutenção e adaptação do sistema a novas necessidades de análise. Além disso, a utilização de um contrato de análise estruturado permite que os dados sejam passados de forma organizada para a camada de visualização, garantindo que a análise seja clara e eficaz.

### 5. **Visualização de Dados (Data Visualization)**

**Processo Desenvolvido:**  
Após a análise dos dados, o próximo passo crucial no fluxo é a visualização, onde os resultados da análise são transformados em gráficos e relatórios visuais que podem ser facilmente interpretados. A classe `ReportsVisualizer` foi desenvolvida para gerar esses gráficos de forma automatizada. A seguir, estão os principais componentes dessa classe:

- **Configuração de Diretório de Saída:** O construtor da classe inicializa o visualizador e configura o diretório onde os gráficos gerados serão salvos. Por padrão, o diretório é chamado `graphs`. Caso o diretório não exista, ele será criado automaticamente.

- **Componentes de Visualização:** Dentro do visualizador, há três componentes principais para gerar diferentes tipos de gráficos:
    - `SalesByRegionVisualizer`: Responsável por gerar gráficos relacionados às vendas por região.
    - `SalesVelocityVisualizer`: Responsável por gerar gráficos relacionados à velocidade de vendas.
    - `SalesByGroupVisualizer`: Responsável por gerar gráficos sobre as vendas por produto e por filial.

- **Geração dos Relatórios Visuais:** O método `generate_reports` recebe o contrato de análise (`AnalyzeContract`), que contém os dados estruturados após a análise, e chama os métodos de visualização para gerar os gráficos. Ele organiza a visualização das informações conforme a análise realizada:
    - **Vendas por Região:** Gera gráficos dos top 10 produtos com maiores vendas por região e os 10 com menores vendas.
    - **Velocidade de Vendas:** Gera gráficos relacionados à velocidade de vendas.
    - **Vendas por Produto e por Filial:** Gera gráficos das vendas agrupadas por produto e filial.

**Solução Encontrada:**  
A principal dificuldade enfrentada foi garantir que os gráficos fossem gerados de forma eficiente e correta, a partir dos dados de análise fornecidos. Para resolver isso, a classe foi dividida em componentes especializados para gerar tipos específicos de gráficos. Essa abordagem modular não só facilita a manutenção, mas também permite que novos tipos de visualizações sejam adicionados facilmente no futuro. Além disso, o uso de um diretório dedicado para salvar os gráficos facilita a organização e acesso aos relatórios gerados.