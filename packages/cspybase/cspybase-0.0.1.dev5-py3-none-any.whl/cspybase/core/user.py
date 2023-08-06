## @package user
## Módulo responsável pela abstração do conceito de usuário no sistema

from cspybase.core.exception import CsPyException

## Classe que representa um usuário
class CsPyUser:

    # Construtor
    # @param self objeto
    # @param connection conexão
    # @param dicionário informativo
    def __init__(self, connection, info):
        self._connection_ = connection
        self._me_ = {}
        self._update_(info)

    ## Consulta o nome do usuário
    ## @param self objeto do tipo usuário.
    ## @return o nome.
    def getname(self):
        return self._me_['name']

    ## Consulta o identificador do usuário
    ## @param self objeto do tipo usuário.
    ## @return o id.
    def getid(self):
        return self._me_['id']

    ## Consulta o login do usuário
    ## @param self objeto do tipo usuário.
    ## @return o login.
    def getlogin(self):
        return self._me_['login']

    # Faz busca de dados no servidor
    # @param self objeto.
    def _fetchdata_(self):
        info = self._connection_.get("v1/users/" + self.getid())
        self._update_(info)

    # Atualiza estruturas internas com base em um dicionário 
    # @param self objeto.
    # @param info diconário informativo
    def _update_(self, info):
        if info is None:
           raise CsPyException("info for user cannot be none!")
        self._me_['id'] = info['id']
        self._me_['name'] = info['name']
        self._me_['login'] = info['login']

    # Consulta representação textual.
    # @param self objeto.
    # @return texto
    def __str__(self):
        return "User: " + self.getname() + " - " + self.getid()

    # Consulta representação textual.
    # @param self objeto.
    # @return texto
    def __repr__(self):
        return self.__str__()
