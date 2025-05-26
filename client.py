import requests, urllib3, getpass
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
            print(dados['mensagem'])
            print("Algoritmo utilizado:", dados['algoritmo'])
        else:
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

        response = requests.post(self.url_autenticacao, json=payload, headers=headers, verify=False)


        if response.status_code == 200:
            token = response.json()["token"]
            self.__token = token
            print("Usuario logado.")
            
        else:
            print("Erro:", response.json()['erro'])
            print("Codigo erro:", response.status_code)

        return
    
    def logout(self) -> None:
        self.__token = ""
        return

if __name__ == "__main__":
    client = Client()
    while True:
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
                break
        except ValueError:
            print("Digite apenas o numero da opcao")
            continue