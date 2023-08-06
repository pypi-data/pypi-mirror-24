## @package connection
## Módulo responsável pelo controle de acesso (conexão) a um sistema CSBase

import http.client
import urllib.parse
import json
import tempfile
import os

import requests

from cspybase.core.exception import CsPyException

## Classe de conexão
class CsPyConnection:

    ## Construtor
    ## @param host endereço do servidor do sistema
    ## @param port porta opcional a ser utilizada (o default é 8010)
    def __init__(self, host, port = 8010):
        self._host_ = host
        self._port_ = port
        self._setunconnected_()
        self._connection_ = http.client.HTTPConnection(host, port)

    ## Inicia uma conexão com base em um login/senha
    ## @param login id/login do usuário
    ## @param password senha
    ## @return True ou False se a conexão foi bem sucedida
    def connectwithlogin(self, login, password):
        try:
           self._setunconnected_()
           params = {'login': login, 'password': password}
           data = self.post("/v1/authentication", params)
           return self._setconnected_(data['accessToken'], data['user']['id'])
        except Exception as e:
           return self._setunconnected_()

    ## Inicia uma conexão com base em um token
    ## @param token token
    ## @return True ou False se a conexão foi bem sucedida
    def connectwithtoken(self, token):
        try:
           self._setunconnected_()
           params = {'userToken': token, 'validationType': 'access' }
           data = self.post("/v1/authentication/token/validation", params)
           if not data['valid']:
              raise Exception("invalid token!") 
           return self._setconnected_(token, 'no-user')
        except Exception as e:
           return self._setunconnected_()

    ## Inicia uma conexão com base em um protocolo de acesso automático com base em uma variável de ambiente 'CS_AUTH_TOKEN'
    ## @return True ou False se a conexão foi bem sucedida
    def autoconnect(self):
        varname = 'CS_AUTH_TOKEN'
        varvalue = os.environ.get(varname)
        if varvalue is None:
           return self._setunconnected_()
        return self.connectwithtoken(varvalue)

    ## Consulta a URL de conexão
    ## @return a URL
    def geturl(self):
        return "http://" + str(self.gethost()) + ":" + str(self.getport())

    ## Consulta a máquina de conexão
    ## @return a máquina
    def gethost(self):
        return self._host_

    ## Consulta a porta da conexão
    ## @return a porta
    def getport(self):
        return self._port_

    ## Consulta o token da conexão
    ## @return o token (se houver) ou None (caso não haja conexão)
    def gettoken(self):
        return self._acesstoken_

    ## Faz a desconexão ao sistema CSBase
    def disconnect(self):
        self._connection_.close()
        self._setunconnected_()

    ## Verifica se há conexão estabelecida
    ## @return indicativo (True ou False)
    def isconnected(self):
        return self._isconnected_

    def post(self, path, parameters):
        return self._request_("POST", path, parameters)


    def get(self, path, parameters):
        return self._request_("GET", path, parameters)


    def delete(self, path, parameters):
        return self._request_("DELETE", path, parameters)

    def touch(self, path, remotefilename):
        tmpname = tempfile.mktemp()
        tmpfile = open(tmpname, "wb")
        tmpfile.close()
        self.upload(path, tmpname, remotefilename)
        os.remove(tmpname)
    
    def upload(self, path, localfilename, remotefilename):
        hds = {}
        if self._isconnected_:
           hds['Authorization'] = "Bearer " + self._acesstoken_
        prs = {}
        fls = {'file' : (remotefilename, open(localfilename, 'rb')) }
        dts = {'uploadType': 'multipart'}
        url = self.geturl() + path
        response = requests.post(url, files=fls, headers=hds, params=prs, data=dts)
        if response.status_code >= 400:
           code = str(response.status_code)
           reason = str(response.reason)
           raise CsPyException("Request post to [" + url + "] failed. Status: " + code + " - " + reason)


    def _encodeparams_(self, dict):
        return urllib.parse.urlencode(dict)


    def _encodeheaders_(self):
        hds = { "Content-type": "application/x-www-form-urlencoded",  "Accept": "application/json" }
        if self._isconnected_:
           hds['Authorization'] = "Bearer " + self._acesstoken_
        return hds

    def _request_(self, type, path, parameters):
        headers = self._encodeheaders_()
        params = self._encodeparams_(parameters)
        self._connection_.request(type, path, params, headers)
        response = self._connection_.getresponse()
        if response.status >= 400:
           raise CsPyException("Request to [" + path + "] failed. Status: " + str(response.status) + " - " + response.reason)
        data = response.read().decode('utf-8')
        if not data or data is None:
           return None
        return json.loads(data)

    def _setconnected_(self, token, userid):
        self._acesstoken_ = token
        self._userid_ = userid
        self._isconnected_ = True
        return True

    def _setunconnected_(self):
        self._acesstoken_ = None
        self._userid_ = None
        self._isconnected_ = False
        return False

    

