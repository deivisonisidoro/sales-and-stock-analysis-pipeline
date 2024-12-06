class LoadError(Exception):
    """
    Exceção personalizada levantada quando ocorre um erro durante o processo de carregamento de dados.

    Esta exceção é usada especificamente para indicar problemas encontrados ao carregar
    dados, como quando os dados não estão no formato esperado ou não podem ser processados.

    Atributos:
        message (str): A mensagem de erro associada à exceção.
        error_type (str): Uma string indicando o tipo de erro, neste caso, 'Erro de Carregamento'.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa a exceção LoadError com uma mensagem de erro específica.

        Args:
            message (str): Uma mensagem de erro descritiva fornecendo mais detalhes
                           sobre a causa da exceção.
        """
        super().__init__(message)
        self.message = message
        self.error_type = "Erro de Carregamento"
