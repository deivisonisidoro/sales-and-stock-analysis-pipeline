from src.analysis.visualization import ReportsVisualizer
from src.driver.dataloader import DataLoader
from src.infra.database_connector import DatabaseConnection
from src.infra.database_repository import DatabaseRepository
from src.stages.analysis.analyze_data import AnalyzeData
from src.stages.extract.extract_data import ExtractData
from src.stages.load.load_data import LoadData
from src.stages.transform.transform_data import TransformData


class MainPipeline:
    """
    Classe que orquestra o pipeline principal de ETL: Extração, Transformação e Carga de dados de vendas e estoque.

    Esta classe coordena as seguintes etapas do pipeline:
    1. Extração dos dados brutos a partir de fontes externas.
    2. Transformação desses dados para formatá-los de acordo com as necessidades do negócio.
    3. Carga dos dados transformados no banco de dados.
    4. Visualização e análise dos dados de vendas para gerar relatórios e insights.

    Atributos:
        __extract_data (ExtractData): Objeto responsável por extrair dados da fonte de dados.
        __transform_data (TransformData): Objeto responsável por transformar os dados extraídos.
        __load_data (LoadData): Objeto responsável por carregar os dados transformados no banco de dados.
        __repository (DatabaseRepository): Objeto responsável pelas operações de banco de dados.
        __sales_visualizer (SalesVisualizer): Objeto responsável pela visualização dos dados de vendas.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe MainPipeline com os componentes necessários para a extração, transformação,
        visualização e carga dos dados no banco de dados.

        Este construtor configura os seguintes objetos do pipeline:
        - Extrator de dados: `ExtractData`
        - Transformador de dados: `TransformData`
        - Carregador de dados: `LoadData`
        - Repositório de banco de dados: `DatabaseRepository`
        - Visualizador de vendas: `SalesVisualizer`
        """
        self.__extract_data = ExtractData(dataloader=DataLoader())
        self.__transform_data = TransformData()
        self.__load_data = LoadData(repository=DatabaseRepository())
        self.__analyze_data = AnalyzeData(repository=DatabaseRepository(), visualizer=ReportsVisualizer())

    def run_pipeline(self) -> None:
        """
        Executa o pipeline completo de ETL: Extrai os dados, transforma-os, carrega-os no banco de dados,
        e visualiza os resultados.

        Este método orquestra as seguintes etapas do pipeline:
        1. Conecta ao banco de dados através do método `DatabaseConnection.connect()`.
        2. Extrai os dados brutos utilizando a classe `ExtractData`.
        3. Transforma os dados extraídos utilizando a classe `TransformData`.
        4. Carrega os dados transformados no banco de dados utilizando a classe `LoadData`.
        5. Visualiza os dados de vendas e gera relatórios utilizando a classe `SalesVisualizer`.

        Args:
            Nenhum

        Return:
            Nenhum

        Raises:
            Exception: Se ocorrer qualquer erro durante a execução de qualquer uma das etapas do pipeline,
            uma exceção será levantada para indicar falhas no processo.
        """
        DatabaseConnection.connect()

        extract_contract = self.__extract_data.extract()

        transform_contract = self.__transform_data.transform(extract_contract)

        self.__load_data.load(transform_contract)

        self.__analyze_data.execute_analysis()
