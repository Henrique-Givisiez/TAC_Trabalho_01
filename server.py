from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
import bcrypt
import jwt
import datetime
import sqlite3

with open("chave_privada.pem", "rb") as f:
    chave_privada_rsa = f.read()

with open("chave_publica.pem", "rb") as f:
    chave_publica_rsa = f.read()

class SimpleRESTHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api-protegida":
            auth_header = self.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                self._set_headers(401)
                self.wfile.write(json.dumps({"erro": "Token nao fornecido"}).encode())
                return            

            token = auth_header.split(" ")[1]
            try:
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

    def do_POST(self):
        if self.path == "/api-autenticacao":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                login = data.get("login")
                senha = data.get("password")
                if login and senha:
                    conn = sqlite3.connect("usuario.db")
                    cursor = conn.cursor()
                    
                    query_select_usuario = "SELECT * FROM Usuario WHERE Login = ? AND Senha = ?"
                    cursor.execute(query_select_usuario, (login, bcrypt.hashpw(senha.encode(), bcrypt.gensalt())))
                    autenticou = cursor.fetchone()
                    conn.close()
                    
                    if autenticou:
                        payload = {
                            "login": login,
                            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
                        }
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

def run(port=4443):
    httpd = HTTPServer(('localhost', port), SimpleRESTHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="chave.pem")

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"Servidor rodando em https://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
