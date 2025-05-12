import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Client:
    def __init__(self):
        self.__token = ""
        self.url_api = "https://localhost:4443/api-protegida"
        self.url_autenticacao = "https://localhost:4443/api-autenticacao"

    def acessa_api_protegida(self) -> None:

        headers = {
                "Authorization": f"Bearer {self.__token}",
                "Accept": "application/json"
            }
        response = requests.get(url=self.url_api, headers=headers, verify=False)   

        if response.status_code == 200:
            dados = response.json()
            print(dados)
        else:
            print("Erro:", response.text['erro'])
            print("Codigo erro:", response.status_code)
            
        return
    
    def autenticacao(self, login: str, senha: str) -> None:
        payload = {
            "login": login,
            "password": senha
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(self.url_autenticacao, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            token = response.json().get("token")
            self.__token = token
            
        else:
            print("Erro de login:", response.status_code)
            print(response.text)

        return
    

if __name__ == "__main__":
    client = Client()
    while True:
        comando = int(input("1. Acessar rota protegida\n2. Fazer autenticação\n0. Sair\n"))
        if comando == 1:
            client.acessa_api_protegida()
        elif comando == 2:
            login = input("Digite o login: ")
            senha = input("Digite a senha: ")
            client.autenticacao(login=login, senha=senha)
        else:
            exit()