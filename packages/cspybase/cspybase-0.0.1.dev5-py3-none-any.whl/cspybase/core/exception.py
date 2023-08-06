## @package exception
## Módulo responsável pela definição de exceções da biblioteca

## Classe de exceção genérica da biblioteca
class CsPyException(Exception):

    # Construtor
    # @param self objeto do tipo exceção
    # @param message mensagem associada a exceção.
    def __init__(self, message):
        super(CsPyException, self).__init__(message)
