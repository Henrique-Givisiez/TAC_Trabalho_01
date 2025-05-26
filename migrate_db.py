# migrate_db.py

# Importa bibliotecas necessárias
import sqlite3  # Para manipular banco de dados SQLite
import bcrypt   # Para fazer o hash seguro da senha

# Cria (ou abre) o banco de dados SQLite chamado "usuario.db"
conn = sqlite3.connect("usuario.db")
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

# Remove a tabela 'Usuario' se ela já existir, garantindo uma nova criação limpa
cursor.execute("DROP TABLE IF EXISTS Usuario")

# Criação da tabela 'Usuario' com duas colunas: Login e Senha
query_cria_tabela = """
                     CREATE TABLE Usuario (
                      Login VARCHAR(255) NOT NULL,
                      Senha VARCHAR(255) NOT NULL
                     );
                    """
cursor.execute(query_cria_tabela)

# Define um usuário padrão para testes
login = "admin"

# Gera um hash seguro da senha "senha123" usando bcrypt
senha = bcrypt.hashpw("senha123".encode(), bcrypt.gensalt())

# Insere o usuário e sua senha já criptografada na tabela
query_cria_usuario = """
                      INSERT INTO 
                       Usuario(Login, Senha) 
                      VALUES
                       (?, ?)   
                     """
cursor.execute(query_cria_usuario, (login, senha))

# Salva as alterações no banco de dados
conn.commit()

# Encerra o cursor e a conexão com o banco
cursor.close()
conn.close()
