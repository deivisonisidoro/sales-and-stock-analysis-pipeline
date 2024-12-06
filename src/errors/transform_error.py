class TransformError(Exception):
    """
    Exceção personalizada levantada quando ocorre um erro durante o processo de transformação de dados.

    Esta exceção é usada especificamente para indicar problemas encontrados ao transformar
    dados, como quando a lógica de transformação falha ou os dados não atendem ao formato
    ou estrutura esperados.

    Atributos:
        message (str): A mensagem de erro associada à exceção.
        error_type (str): Uma string indicando o tipo de erro, neste caso, 'Erro de Transformação'.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa a exceção TransformError com uma mensagem de erro específica.

        Args:
            message (str): Uma mensagem de erro descritiva fornecendo mais detalhes
                           sobre a causa da exceção.
        """
        super().__init__(message)
        self.message = message
        self.error_type = "Erro de Transformação"
