from src.analysis.visualization import SalesVisualizer
from src.driver.dataloader import DataLoader
from src.infra.database_connector import DatabaseConnection
from src.infra.database_repository import DatabaseRepository
from src.stages.contracts.load_contract import LoadContract
from src.stages.extract.extract_data import ExtractData
from src.stages.load.load_data import LoadData
from src.stages.transform.transform_data import TransformData


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
        self.__transform_data = TransformData()
        self.__load_data = LoadData(repository=DatabaseRepository())
        self.__repository = DatabaseRepository()
        self.__sales_visualizer = SalesVisualizer()

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

        transform_contract = self.__transform_data.transform(extract_contract)

        self.__load_data.load(transform_contract)

        sales_velocity = self.__repository.find(table_name="sales_velocity")
        sales_by_region = self.__repository.find(table_name="sales_by_region")
        sales = self.__repository.find(table_name="sales")

        load_contractor = LoadContract(sales_by_region=sales_by_region, sales_velocity=sales_velocity, sales=sales)

        self.__sales_visualizer.analyze(load_contractor)
