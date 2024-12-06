from tarfile import ExtractError

from src.driver.interface.dataloader_interface import DataLoaderInterface
from src.stages.contracts.extract_contract import ExtractContract


class ExtractData:
    """
    Classe de serviço responsável por extrair e preparar dados usando um DataLoader.

    Esta classe encapsula a lógica para carregar dados de múltiplas fontes predefinidas
    e retornar os dados processados em um formato estruturado.

    Atributos:
        __dataloader (DataLoaderInterface): Uma instância de um DataLoader que implementa o DataLoaderInterface.
    """

    def __init__(self, dataloader: DataLoaderInterface) -> None:
        """
        Inicializa o serviço ExtractData.

        Args:
            dataloader (DataLoaderInterface): A instância do DataLoader responsável por recuperar os dados.
        """
        self.__dataloader = dataloader

    def extract(self) -> ExtractContract:
        """
        Extrai dados do DataLoader e os encapsula em um ExtractContract.

        Este método chama o método `extract_all` do DataLoader para recuperar os dados,
        e então cria um ExtractContract contendo os dados e a data da extração atual.

        Retorna:
            ExtractContract: Um contrato contendo os dados extraídos e a data da extração.

        Raise:
            ExtractError: Se ocorrer um erro durante o processo de extração de dados.
        """
        try:
            data = self.__dataloader.extract_all()

            return ExtractContract(
                data=data,
            )
        except Exception as exception:
            raise ExtractError(str(exception)) from exception
