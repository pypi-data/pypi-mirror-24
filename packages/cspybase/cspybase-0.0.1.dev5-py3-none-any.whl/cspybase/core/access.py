## @package access
## Módulo responsável pelo acesso (já estabelecido por conexão) a um sistema CSBase

from cspybase.core.project import CsPyProject
from cspybase.core.user import CsPyUser
from cspybase.core.exception import CsPyException

## Classe que representa um acesso bem sucedido a um servidor.
class CsPyAccess:

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        if not connection.isconnected():
           raise CsPyException('invalid offline connection!') 
        self._connection_ = connection
        self._projectspath_ = "/v1/projects"
        self._userspath_ = "/v1/users"

    ## Consulta a lista de projetos disponíveis para este acesso
    ## @param self objeto do tipo acesso
    ## @return uma tupla com os projetos.
    def getprojects(self):
        prjs = self._connection_.get(self._projectspath_, {})
        list = []
        it = iter(prjs)
        for p in it:
            list.append(CsPyProject(self._connection_, p))
        return tuple(list)

    ## Cria um novo projeto
    ## @param self objeto do tipo acesso
    ## @param name nome do novo projeto a ser criado
    ## @param description descrição do novo projeto (opcional)
    ## @return o novo projeto criado
    def createproject(self, name, description = None):
        if description is None:
           description = name
        params = {'name': name, 'description': description}
        info = self._connection_.post(self._projectspath_, params)
        return CsPyProject(self._connection_, info)

    ## Retorna um projeto com base em seu nome
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser pesquisado
    ## @return o projeto ou None (caso este não seja encontrado)
    def getproject(self, name):
        prjs = self.getprojects()
        for p in prjs:
            if p.getname() == name:
               return p
        return None

    ## Apaga um projeto com base em seu nome.
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser apagado
    def deleteproject(self, name):
        prj = self.getproject(name)
        if prj is not None:
           prjid = prj.getid()
           self._connection_.delete("/v1/projects/" + prjid, {})

    ## Consulta a lista de usuários do sistema
    ## @param self objeto do tipo acesso
    ## @return uma tupla com objeto do tipo usuário
    def getusers(self):
        usrs = self._connection_.get(self._userspath_, {})
        list = []
        it = iter(usrs)
        for u in it:
            list.append(CsPyUser(self._connection_, u))
        return tuple(list)

