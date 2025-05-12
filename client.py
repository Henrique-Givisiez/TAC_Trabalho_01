import requests, getpass

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
        response = requests.get(self.url_api, headers, verify=False)   

        if response.status_code == 200:
            dados = response.json()
            print(dados)
        else:
            print("Erro:", response.status_code)
            print(response.text)

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

        response = requests.post(self.url_autenticacao, json=payload, headers=headers)

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
            senha = getpass.getpass(input("Digite a senha: "))
            client.autenticacao(login=login, senha=senha)
        else:
            exit()