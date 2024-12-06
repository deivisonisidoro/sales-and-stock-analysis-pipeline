from src.analysis.analyze_data import SalesByRegionAnalyzer
from src.analysis.visualization import SalesVisualizer
from src.driver.dataloader import DataLoader
from src.infra.database_connector import DatabaseConnection
from src.infra.database_repository import DatabaseRepository
from src.stages.extract.extract_data import ExtractData
from src.stages.load.load_data import LoadData
from src.stages.transform.data_cleaner import DataCleaner
from src.stages.transform.sales_transform import SalesTransformer
from src.stages.transform.stock_transformer import StockTransformer


class MainPipeline:
    """
    Classe que orquestra o pipeline principal de ETL: Extração, Transformação e Carga de dados de vendas e estoque.

    Esta classe coordena o processo de extração dos dados brutos, transformação desses dados, e carga no banco de dados.
    Também lida com a visualização dos dados processados para análise.

    Atributos:
        __extract_data (ExtractData): Objeto responsável por extrair dados da fonte de dados.
        __sales_transform (SalesTransformer): Objeto responsável por transformar os dados de vendas.
        __stock_transform (StockTransformer): Objeto responsável por transformar os dados de estoque.
        __sales_visualizer (SalesVisualizer): Objeto responsável por visualizar os dados de vendas.
        __load_data (LoadData): Objeto responsável por carregar os dados transformados no banco de dados.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe MainPipeline com os componentes necessários para a extração, transformação,
        visualização e carga dos dados no banco de dados.

        Argumentos:
            Nenhum
        """
        self.__extract_data = ExtractData(dataloader=DataLoader())
        self.__sales_transform = SalesTransformer()
        self.__stock_transform = StockTransformer()
        self.__sales_visualizer = SalesVisualizer()
        self.__load_data = LoadData(DatabaseRepository())

    def run_pipeline(self) -> None:
        """
        Executa o pipeline completo de ETL: Extrai os dados, transforma-os, carrega-os no banco de dados,
        e visualiza os resultados.

        Este método orquestra as seguintes etapas:
        1. Conecta ao banco de dados.
        2. Extrai os dados brutos usando a classe ExtractData.
        3. Transforma os dados extraídos utilizando várias classes de transformação.
        4. Carrega os dados transformados no banco de dados usando LoadData.
        5. Visualiza os dados de vendas usando SalesVisualizer.

        Argumentos:
            Nenhum

        Retorna:
            Nenhum

        Raise:
            Exception: Se ocorrer qualquer erro durante a execução do pipeline, uma exceção será levantada.
        """
        DatabaseConnection.connect()

        extract_contract = self.__extract_data.extract()

        estoque_disponivel = self.__stock_transform.calculate_available_stock(
            DataCleaner.clean_data(extract_contract.data["stock"])
        )
        vendas = DataCleaner.clean_data(extract_contract.data["sales"])
        velocidade_venda = self.__sales_transform.calculate_sales_velocity(vendas, estoque_disponivel)
        vendas_por_regiao = SalesByRegionAnalyzer.calculate_sales_by_region(vendas, extract_contract.data["store"])

        self.__load_data.load(
            {
                "estoque_disponivel": estoque_disponivel,
                "velocidade_venda": velocidade_venda,
                "vendas_por_regiao": vendas_por_regiao,
            }
        )

        self.__sales_visualizer.plot_sales_by_region(vendas_por_regiao)
        self.__sales_visualizer.plot_sales_velocity(velocidade_venda)
        self.__sales_visualizer.plot_sales_by_group(velocidade_venda, vendas)
