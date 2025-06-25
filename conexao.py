import mysql.connector

conexao = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "rai01548",
    database = "controle_de_financas"
)

print(f'conexao com mysql feita com sucesso')
