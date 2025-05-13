import sqlite3, bcrypt

conn = sqlite3.connect("usuario.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Usuario")
query_cria_tabela = """
                     CREATE TABLE Usuario (
                      Login VARCHAR(255) NOT NULL,
                      Senha VARCHAR(255) NOT NULL
                     );
                    """
cursor.execute(query_cria_tabela)

login = "admin"
senha = bcrypt.hashpw("senha123".encode(), bcrypt.gensalt())
query_cria_usuario = """
                      INSERT INTO 
                       Usuario(Login, Senha) 
                      VALUES
                       (?, ?)   
                     """
cursor.execute(query_cria_usuario, (login, senha))

conn.commit()
cursor.close()
conn.close()