
# Trabalho Prático 01 - Autenticação e Assinatura Digital

## Descrição

Este projeto implementa uma aplicação cliente-servidor segura, utilizando autenticação com tokens JWT assinados digitalmente. O sistema permite a escolha dinâmica entre dois algoritmos de assinatura:

- **HMAC-SHA256 (HS256)** — baseado em chave secreta compartilhada.
- **RSA-SHA256 (RS256)** — baseado em criptografia assimétrica.

A comunicação entre cliente e servidor é protegida por **TLS (HTTPS)**, garantindo a confidencialidade e a integridade dos dados.

---

## Funcionalidades

- Autenticação de usuário via JWT.
- Escolha dinâmica do algoritmo de assinatura (HMAC ou RSA).
- Acesso a rota protegida mediante validação do token.
- Logout com remoção do token armazenado.
- Criptografia de transporte com certificado digital autoassinado.
- Análise prática com captura de pacotes via Wireshark.

---

## Como Executar

1. **Geração do certificado:**

```bash
python gerar_certificado.py
```

2. **Executar o servidor:**

```bash
python server.py
```

3. **Executar o cliente:**

```bash
python client.py
```

4. No cliente, siga o menu para:

- Fazer autenticação.
- Escolher entre HS256 ou RS256.
- Acessar a rota protegida.
- Realizar logout.

---

## Requisitos

- Python 3.8+
- Bibliotecas:
  - `bcrypt`
  - `pyjwt`
  - `cryptography`
  - `requests`
  - `urllib3`
  - `sqlite3`

Instale as dependências com:

```bash
pip install bcrypt pyjwt cryptography requests
```

---

## Observações

- O certificado gerado é autoassinado, adequado apenas para ambientes de desenvolvimento.
- O servidor realiza a verificação automática do algoritmo utilizado na assinatura do token.
- A análise de pacotes com Wireshark demonstra a importância do TLS na proteção dos dados transmitidos.

---

## Autores

- Gabriel Kenji Andrade Mizuno — 202006386
- Henrique Givisiez dos Santos — 211027563

Departamento de Ciência da Computação  
Universidade de Brasília — 2025
