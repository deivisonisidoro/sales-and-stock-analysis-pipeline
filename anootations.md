### **Objetivo Geral**
Você precisa realizar uma análise de dados utilizando suas habilidades e ferramentas disponíveis. O objetivo principal inclui:  

1. **Armazenar dados CSV em um banco de dados**:
   - Subir os dados contidos nos arquivos CSV para o banco de dados **BigQuery** (ou outro de sua escolha).  
   - Usar Python para realizar as etapas de **extração**, **tratamento**, **carga** e **cálculo de indicadores**.

2. **Apresentar os resultados**:
   - Após concluir a análise e o processamento dos dados, os resultados encontrados devem ser apresentados de forma clara e visual.  
   - Você pode usar ferramentas como **PowerPoint**, **Power BI**, ou **Excel** para criar gráficos, tabelas e relatórios que mostrem os insights e conclusões.

---

### **Orientações**
1. **Arquivos fornecidos**:
   - Você receberá **quatro arquivos CSV**, cada um com informações diferentes que deverão ser carregadas no BigQuery.  
   - Cada tabela deve ser tratada e carregada separadamente, mas no final, devem ser **cruzadas** (ou seja, relacionadas) utilizando **views** ou consultas **SQL**.  

2. **Desafios nos dados**:
   - Alguns dados podem estar **duplicados ou ausentes** em algumas tabelas.  
   - Você será avaliado pela forma como trata essas exceções (exemplo: remoção de duplicatas, preenchimento de valores ausentes, etc.).

---

### **Descrição das Tabelas**

1. **Estoque Total**:
   - Contém a quantidade total de cada produto (identificado por cor e tamanho) em cada filial, organizada por data.
   - Chave primária: **Produto-cor**.

2. **Estoque Trânsito**:
   - Similar ao estoque total, mas representa os itens que estão em trânsito.  
   - Chave primária: **Produto-cor**.

3. **Tabela a ser criada**:
   - Uma nova tabela deve ser criada com o **estoque disponível**, calculado como:
     - **Estoque Disponível = Estoque Total - Estoque Trânsito**
   - Nesse cálculo, todos os tamanhos devem ser **agregados** (somados) no nível de **produto-cor**.

4. **Produtos**:
   - Essa tabela contém a lista de produtos e cores que devem ser analisados.  
   - **Importante**: Apenas os produtos listados aqui devem ser considerados; os demais devem ser descartados.

5. **Venda**:
   - Registra as vendas de produtos no período fornecido.  
   - Campo importante: **VENDA_PECAS** (quantidade vendida).  
   - Vendas negativas representam **devoluções de produtos**.

6. **Lojas**:
   - Contém a lista de filiais com seus respectivos nomes e códigos.

7. **Velocidade de Venda**:
   - Crie uma tabela com o cálculo da **velocidade de venda em 14 dias**:
     - **Velocidade de venda = Vendas em peças / Dias de estoque disponível**  
     - **Atenção**: Não considere os dias em que o estoque foi zero.

---

### **Análises Sugeridas**
1. **Fluxograma**:
   - Crie um fluxograma que descreva o processo de extração, tratamento e carregamento dos dados.  
   - Explique detalhadamente as etapas que você desenvolveu e as soluções que encontrou.

2. **Perguntas a serem respondidas**:
   - Quais regiões tiveram mais vendas?  
   - Quais tiveram menos vendas?  
   - Quais produtos (artigos e cores) possuem maior velocidade de venda?  
   - Quais grupos de produtos ou filiais apresentam melhor desempenho?  

3. **Outras análises**:
   - Além das perguntas sugeridas, você pode realizar análises adicionais que considerar relevantes para o entendimento do negócio.

---

### **O que será avaliado**
1. **Workflow**:
   - O fluxo para tratamento dos dados: desde a extração, passando pelo tratamento e carregamento no banco.

2. **Soluções implementadas**:
   - Sua abordagem para tratar dados inconsistentes ou ausentes.  
   - Criatividade nas soluções e clareza na explicação das etapas.

3. **Complexidade das análises**:
   - Profundidade das análises realizadas e a relevância das conclusões apresentadas.

4. **Documentação**:
   - Detalhamento do processo e explicação clara do passo a passo seguido.

---

Essa explicação cobre o propósito do desafio, o que você deve fazer e como será avaliado.