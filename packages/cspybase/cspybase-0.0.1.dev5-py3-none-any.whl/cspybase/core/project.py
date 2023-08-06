## @package project
## Módulo responsável pela abstração do conceito de projetos no sistema

from cspybase.core.user import CsPyUser
from cspybase.core.file import CsPyFile
from cspybase.core.exception import CsPyException

## Classe que representa um projeto dentro do servidor.
class CsPyProject:

    # Construtor
    # @param self objeto do tipo arquivo/diretório
    # @param connection conexão
    # @param info dicionário informativo dos dados o arquivo/diretório
    def __init__(self, connection, info):
        self._connection_ = connection
        self._me_ = {}
        self._update_(info)

    ## Consulta o nome do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o nome.
    def getname(self):
        return self._me_['name']

    ## Consulta o identificador do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o id.
    def getid(self):
        return self._me_['id']

    ## Consulta o usuário dono do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o usuário.
    def getowner(self):
        return self._me_['owner']

    ## Consulta o diretório-raiz do projeto
    ## @param self objeto do tipo projeto.
    ## @return o diretório.
    def getroot(self):
        info = self._connection_.get("/v1/projects/" + self.getid() + "/files/root/metadata", {})
        if info is None:
            raise CsPyException("bad info for project root!")
        return CsPyFile(self._connection_, self.getid(), info.get('file'))

    ## Faz busca de dados no servidor
    ## @param self objeto.
    def _fetchdata_(self):
        info = self._connection_.get("v1/projects/" + self.getid(), {})
        self._update_(info)

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info diconário informativo
    def _update_(self, info):
        if info is None:
            raise CsPyException("info for project cannot be none!")
        self._me_['id'] = info['id']
        self._me_['name'] = info['name']
        self._me_['description'] = info['description']
        self._me_['owner'] = CsPyUser(self._connection_, info['owner'])

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        return "Project: " + self.getname() + " - " + self.getid()

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()



