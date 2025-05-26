# client.py

# Importa bibliotecas necessárias
import requests          # Realiza requisições HTTP
import urllib3           # Biblioteca de suporte HTTP para desabilitar alertas SSL
import getpass           # Para ocultar a senha digitada no terminal

# Desabilita o aviso de certificado SSL não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Classe que representa o cliente da aplicação
class Client:
    def __init__(self):
        self.__token = ""  # Armazena o token JWT após autenticação
        self.url_api = "https://localhost:4443/api-protegida"         # URL da rota protegida
        self.url_autenticacao = "https://localhost:4443/api-autenticacao"  # URL da rota de autenticação

    # Método que tenta acessar a API protegida usando o token JWT
    def acessa_api_protegida(self) -> None:
        headers = {
            "Authorization": f"Bearer {self.__token}",  # Inclui o token no header Authorization
            "Accept": "application/json"
        }

        # Realiza uma requisição GET para a rota protegida
        response = requests.get(url=self.url_api, headers=headers, verify=False)

        # Se a resposta for 200 (OK), imprime a mensagem do servidor
        if response.status_code == 200:
            dados = response.json()
            print(dados['mensagem'])
            print("Algoritmo utilizado:", dados['algoritmo'])
        else:
            # Caso contrário, imprime erro e o código HTTP retornado
            print("Erro:", response.json()['erro'])
            print("Codigo erro:", response.status_code)

        return
    
    def autenticacao(self, login: str, senha: str,algoritmo) -> None:
        payload = {
            "login": login,
            "password": senha,
            "algoritmo":algoritmo
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Envia uma requisição POST com login e senha para obter o token
        response = requests.post(self.url_autenticacao, json=payload, headers=headers, verify=False)


        if response.status_code == 200:
            # Armazena o token retornado pelo servidor
            token = response.json()["token"]
            self.__token = token
            print("Usuario logado.")
        else:
            # Exibe mensagem de erro
            print("Erro:", response.json()['erro'])
            print("Codigo erro:", response.status_code)

        return

    # Método para "deslogar" o usuário, limpando o token armazenado
    def logout(self) -> None:
        self.__token = ""
        return

# Bloco principal: interface interativa em terminal
if __name__ == "__main__":
    client = Client()
    while True:
        # Exibe menu de opções
        comando = int(input("1) Acessar rota protegida\n2) Fazer autenticação\n3) Fazer logout\n0) Sair\n"))
        try:
            if comando == 1:
                client.acessa_api_protegida()
            elif comando == 2:
                login = input("Digite o login: ")
                senha = getpass.getpass("Digite a senha: ")
                algoritmo = input("Escolha o algoritmo (RS256/HS256): ").strip().upper()
                if algoritmo not in ["RS256", "HS256"]:
                    print("Algoritmo inválido. Usando RS256 por padrão.")
                    algoritmo = "RS256"
                client.autenticacao(login=login, senha=senha, algoritmo=algoritmo)


            elif comando == 3:
                client.logout()
            else:
                break  # Sai do programa
        except ValueError:
            print("Digite apenas o numero da opcao")
            continue
