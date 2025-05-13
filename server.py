# server.py

# Importa classes e módulos necessários
from http.server import HTTPServer, BaseHTTPRequestHandler  # servidor HTTP básico
import ssl                  # módulo para habilitar HTTPS (SSL/TLS)
import json                 # manipulação de dados JSON
import bcrypt               # hashing seguro de senhas
import jwt                  # manipulação de JWTs (JSON Web Tokens)
import datetime             # controle de data e hora (expiração de tokens)
import sqlite3              # acesso a banco de dados SQLite

# Lê a chave privada RSA do arquivo, usada para assinar tokens
with open("chave_privada.pem", "rb") as f:
    chave_privada_rsa = f.read()

# Lê a chave pública RSA do arquivo, usada para verificar assinaturas de tokens
with open("chave_publica.pem", "rb") as f:
    chave_publica_rsa = f.read()

# Classe que define o tratamento das requisições recebidas
class SimpleRESTHandler(BaseHTTPRequestHandler):

    # Método auxiliar para configurar os headers da resposta HTTP
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    # Método que lida com requisições GET
    def do_GET(self):
        if self.path == "/api-protegida":
            # Recupera o header "Authorization"
            auth_header = self.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                self._set_headers(401)
                self.wfile.write(json.dumps({"erro": "Token nao fornecido"}).encode())
                return

            # Extrai o token do header
            token = auth_header.split(" ")[1]
            try:
                # Verifica e decodifica o token JWT usando a chave pública RSA
                decoded = jwt.decode(token, chave_publica_rsa, algorithms=["RS256"])
                usuario = decoded.get("login")
                self._set_headers()
                self.wfile.write(json.dumps({"mensagem": f"Voce esta logado, {usuario}"}).encode())

            except jwt.ExpiredSignatureError:
                self._set_headers(401)
                self.wfile.write(json.dumps({"erro": "Token expirado"}).encode())

            except jwt.InvalidTokenError:
                self._set_headers(401)
                self.wfile.write(json.dumps({"erro": "Token invalido"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"erro": "Caminho nao encontrado"}).encode())

    # Método que lida com requisições POST
    def do_POST(self):
        if self.path == "/api-autenticacao":
            # Lê o corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # Decodifica o JSON enviado pelo cliente
                data = json.loads(post_data.decode())
                login = data.get("login")
                senha = data.get("password")

                if login and senha:
                    # Acessa o banco de dados para buscar o hash da senha
                    conn = sqlite3.connect("usuario.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT Senha FROM Usuario WHERE Login = ?", (login,))
                    senha_confere = bcrypt.checkpw(senha.encode(), cursor.fetchone()[0])
                    conn.close()

                    if senha_confere:
                        # Cria o payload do token com login e expiração
                        payload = {
                            "login": login,
                            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
                        }
                        # Gera e assina o token com RSA
                        token = jwt.encode(payload, chave_privada_rsa, algorithm="RS256")

                        self._set_headers()
                        self.wfile.write(json.dumps({"mensagem": "Login bem-sucedido", "token": token}).encode())
                    else:
                        self._set_headers(401)
                        self.wfile.write(json.dumps({"erro": "Credenciais invalidas"}).encode())
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"erro": "Login e senha são obrigatorios"}).encode())

            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"erro": "Requisicao invalida"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"erro": "Caminho nao encontrado"}).encode())

# Função que inicializa o servidor HTTPS
def run(port=4443):
    httpd = HTTPServer(('localhost', port), SimpleRESTHandler)

    # Cria o contexto SSL (HTTPS) e carrega o certificado e chave privada
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="chave.pem")

    # Aplica o contexto SSL ao socket do servidor
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Servidor rodando em https://localhost:{port}")
    httpd.serve_forever()

# Executa o servidor ao rodar o script
if __name__ == "__main__":
    run()
