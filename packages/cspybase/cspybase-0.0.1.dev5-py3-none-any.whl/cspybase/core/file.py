## @package file
## Módulo responsável pela abstração do conceito de arquivos/diretórios no sistema

import shutil
import urllib.request
import tempfile
import os

from cspybase.core.user import CsPyUser
from cspybase.core.exception import CsPyException

## Classe que representa um arquivo ou diretório
class CsPyFile:

    # Construtor
    # @param self objeto do tipo arquivo/diretório
    # @param connection conexão
    # @param projectid identificador do projeto
    # @param info dicionário informativo dos dados o arquivo/diretório
    def __init__(self, connection, projectid, info):
        if info is None:
           raise CsPyException("bad info for file constructor!")
        if projectid is None:
           raise CsPyException("bad projectid for file constructor!")
        self._written_ = False
        self._tempfile_ = None
        self._tempfilename_ = None
        self._connection_ = connection
        self._projectid_ = projectid
        self._me_ = {}
        self._children_ = []
        self._updateme_(info)


    ## Consulta o nome do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return o nome
    def getname(self):
        return self._me_['name']

    ## Consulta o identificador único do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id
    def getid(self):
        return self._me_['id']

    ## Consulta se o objeto representa um diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return indicativo (True ou False)
    def isfolder(self):
        return self._me_['isfolder']

    ## Consulta se o objeto representa um arquivo
    ## @param self objeto do tipo arquivo/diretório
    ## @return indicativo (True ou False)
    def isfile(self):
        return not self.isfolder()

    ## Consulta o identificador único do pai (parent)
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id do diretório pai
    def getparentid(self):
        return self._me_['parentid']

    ## Consulta o identificador único do projeto a que pertence o arquivo/diretório.
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id do projeto
    def getprojectid(self):
        return self._projectid_

    ## Consulta o path do arquivo/diretório dentro do projeto
    ## @param self objeto do tipo arquivo/diretório
    ## @return o path
    def getpath(self):
        return self._me_['path']

    ## Consulta o usuário criador do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return um objeto representativo do usuário.
    def getcreator(self):
        return self._me_['creator']

    ## Consulta a descrição do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return a descrição textual
    def getdescription(self):
        return self._me_['description']

    ## Consulta a lista de filhos de um diretório
    ## @param self objeto do tipo diretório
    ## @return a lista de objetos do tipo arquivo/diretório
    def list(self):
        self._checkisfolder_()
        self._fetchdata_()
        return self._children_

    ## Cria um novo diretório dentro do objeto 'self' diretório
    ## @param self objeto do tipo diretório
    ## @param name nome do novo diretório a ser criado.
    ## @return um objeto que representa o novo diretório
    def mkdir(self, name):
        self._checkisfolder_()
        params = {'name': name}
        info = self._connection_.post(self._getmypath_() + "/folder", params)
        file = CsPyFile(self._connection_, self.getprojectid(), info)
        return file

    ## Apaga o arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    def delete(self):
        info = self._connection_.delete(self._getmypath_(), {})

    ## Retorna um filho (com base em um nome) do objeto do tipo diretório
    ## @param self objeto do tipo diretório.
    ## @param name nome a ser pesquisado.
    ## @return o objeto do tipo arquivo/diretório ou None (se não houver)
    def getfile(self, name):
        self._checkisfolder_()
        children = self.list()
        for c in children:
            if c.getname() == name:
               return c
        return None

    ## Retorna um objeto do tipo diretório que representa o pai deste arquivo/diretório.
    ## @param self objeto do tipo arquivo/diretório
    ## @return objeto do tipo diretório
    def getparent(self):
        pid = self.getparentid()
        pinfo = self._connection_.get(self._getparentpath_() + "/metadata", {})
        if pinfo is None:
           return None
        info = pinfo.get('file')
        parent = CsPyFile(self._connection_, self.getprojectid(), info)
        return parent

    ## Retorna um link associado ao objeto do tipo arquivo/diretório dentro do servidor
    ## @param self objeto do tipo arquivo/diretório
    ## @return um texto com a URL
    def getlink(self):
        self._checkisnotfolder_()
        info = self._connection_.get(self._getmypath_() + "/link", {})
        if info is None:
           return None
        url = info.get('url')
        return url

    ## Faz o download do objeto do tipo arquivo.
    ## @param self objeto do tipo arquivo/diretório
    ## @param filename nome do arquivo aonde será feito o download.
    def download(self, filename):
        self._checkisnotfolder_()
        url = self.getlink()
        if url is None:
           return CsPyException("unable do find a link to file")
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as outfile:
             shutil.copyfileobj(response, outfile)

    ## Cria um novo arquivo dentro do objeto do tipo diretório (não faz nada se já existir).
    ## @param self objeto do tipo arquivo/diretório
    ## @param filename nome do arquivo a ser criado.
    ## @return o novo arquivo criado ou já existente
    def touch(self, filename):
        self._checkisfolder_()
        file = self.getfile(filename)
        if file is not None:
           return file
        self._connection_.touch(self._getmypath_(), filename)
        self._fetchdata_()
        return self.getfile(filename)

    ## Abre um arquivo dentro do objeto do tipo diretório (cria se não existir)
    ## @param self objeto do tipo diretório
    ## @param filename nome do arquivo a ser aberto
    ## @param accessmode modo de acesso ao arquivo.
    ## @param buffering tamnaho do buffer (opcional)
    def openfile(self, filename, accessmode, buffering = None):
        file = self.touch(filename)
        file.open(accessmode, buffering)
        return file

    ## Abre o arquivo 
    ## @param self objeto do tipo arquivo
    ## @param accessmode modo de acesso ao arquivo.
    ## @param buffering tamnaho do buffer (opcional)
    def open(self, accessmode, buffering = None):
        self._checkisnotfolder_()
        parent = self.getparent()
        parent.touch(self.getname())

        buffering = 1024 if buffering is None else buffering
        tmpname = tempfile.mktemp()
        tmpfile = open(tmpname, "wb", 1024 * 1024)
        url = self.getlink()
        if url is None:
           return CsPyException("unable do find a link to file")
        with urllib.request.urlopen(url) as response:
             shutil.copyfileobj(response, tmpfile)

        tmpfile.close()

        self._tempfile_ = open(tmpname, accessmode, buffering)
        self._tempfilename_ = tmpname

    ## Fecha o arquivo.
    ## @param self objeto do tipo arquivo.
    def close(self):
        if self._tempfile_ is None or self.isfolder():
           return
        self._tempfile_.close()
        self._tempfile_ = None
        if self._written_: 
           self._connection_.upload(self._getparentpath_(), self._tempfilename_, self.getname())
        os.remove(self._tempfilename_)
        self._tempfilename_ = None

    ## Escreve bytes no arquivo
    ## @param self objeto do tipo arquivo.
    ## @param data dados a serem gravados.
    ## @return número de bytes escritos
    def write(self, data):
        self._written_ = True
        self._checkopenedfile_()
        self._checkisnotfolder_()
        return self._tempfile_.write(data)

    ## Lê bytes do arquivo.
    ## @param self objeto do tipo arquivo.
    ## @param count quantidade de bytes a serem lidos (opcional)
    ## @return número de bytes escritos.
    def read(self, count = -1):
        self._checkopenedfile_()
        self._checkisnotfolder_()
        return self._tempfile_.read(count)

    ## Lê uma linha inteira de do objeto arquivo.
    ## @param self objeto do tipo arquivo.
    ## @param size quantidade máxima de bytes a serem lidos (opcional).
    ## @return texto com um '\n' no final da string -- o newline é omitido caso seja a última linha do arquivo.
    def readline(self, size = -1):
        self._checkopenedfile_()
        self._checkisnotfolder_()
        return self._tempfile_.readline(size)

    ## Altera a posição corrente de I/O do obejto do tipo arquivo.    
    ## @param self objeto do tipo arquivo.
    ## @param offset desclocament dentro de uma referência (whence).
    ## @param whence referência opcional dentro do arquivo (0, começo do arquivo; 1, posição corrente, 2, fim do arquivo).
    def seek(self, offset, whence = 0):
        self._checkopenedfile_()
        self._checkisnotfolder_()
        return self._tempfile_.seek(offset, whence)
    
    ## Consulta a posição corrente de I/O do objeto do tipo arquivo.
    ## @param self objeto do tipo arquivo.
    ## @return a posição
    def tell(self):
        self._checkopenedfile_()
        self._checkisnotfolder_()
        return self._tempfile_.tell()

    ## Testa se o arquivo está aberto
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _checkopenedfile_(self):
        if self._tempfile_ is None:
           raise CsPyException("file is not opened!")

    ## Testa se o objeto não é diretório
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _checkisnotfolder_(self):
        if self.isfolder():
           raise CsPyException("operation allowed only to non-directories!")

    ## Testa se o objeto é diretório
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _checkisfolder_(self):
        if not self.isfolder():
           raise CsPyException("operation allowed only to directories!")

    ## Consulta path REST do objeto diretório-pai no servidor
    ## @param self objeto.
    ## @return path
    def _getparentpath_(self):
        return self._getpath_(self.getprojectid(), self.getparentid())

    ## Consulta path REST do objeto arquivo/diretório no servidor
    ## @param self objeto.
    ## @return path
    def _getmypath_(self):
        return self._getpath_(self.getprojectid(), self.getid())

    ## Consulta path REST no servidor de um projeto/arquivo
    ## @param self objeto.
    ## @param projectid id do projeto.
    ## @param fileid id do arquivo.
    ## @return path
    def _getpath_(self, projectid, fileid):
        return "/v1/projects/" + str(projectid) + "/files/" + str(fileid)

    ## Faz busca de dados no servidor
    ## @param self objeto.
    def _fetchdata_(self):
        info = self._connection_.get(self._getmypath_() + "/metadata", {})
        self._update_(info)

    ## Atualiza todos dados (internos e dos filhos) com base em dicionário informativo
    ## @param self objeto.
    def _update_(self, info):
        finfo = info.get('file')
        self._updateme_(finfo)
        cinfos = info.get('content')
        self._updatechildren_(cinfos)

    ## Atualiza dados internos com base em dicionário informativo
    ## @param self objeto.
    def _updateme_(self, info):
        if info is None:
           raise CsPyException("bad info for file updateme!")
        id = info.get('id')
        if id is None:
           raise CsPyException("no id for file updateme!")

        self._me_['id'] = id
        self._me_['name'] = info.get('name')
        self._me_['isfolder'] = info.get('isFolder')
        self._me_['description'] = info.get('description')
        self._me_['underconstruction'] = info.get('isUnderConstruction')
        self._me_['path'] = info.get('path')
        self._me_['parentid'] = info.get('parentId')
        userinfo = info.get('createdBy')
        if userinfo is not None:
           self._me_['creator'] = CsPyUser(self._connection_, userinfo)

    ## Atualiza dados dos filhos com base em lista de dicionários informativos
    ## @param self objeto.
    def _updatechildren_(self, infos):
        self._children_ = [];
        for info in infos:
            if info is not None:
               file = CsPyFile(self._connection_, self.getprojectid(), info)
               self._children_.append(file)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        return "File: " + self.getname() + " - " + self.getid()

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()



