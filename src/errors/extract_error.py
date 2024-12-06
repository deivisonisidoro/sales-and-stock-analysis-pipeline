class ExtractError(Exception):
    """
    Classe personalizada para exceções encontradas durante a extração de dados.

    Atributos:
        message (str): Uma mensagem descritiva do erro.
        error_type (str): Uma string fixa identificando o tipo de erro como 'Erro de Extração'.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa a exceção ExtractError com uma mensagem.

        Args:
            message (str): Uma mensagem descritiva do erro.
        """
        super().__init__(message)
        self.message = message
        self.error_type = "Erro de Extração"
