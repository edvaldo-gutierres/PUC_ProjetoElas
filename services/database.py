# Conexão com o banco de dados MySQL
import mysql.connector

# Conectar ao banco de dados MySQL
# conn = mysql.connector.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='1234',
#     database='db_projetoelas'
# )

conn = mysql.connector.connect(
    host='containers-us-west-46.railway.app',
    port=6409,
    user='root',
    password='wMzbX6qodmA8SWLDH8j0',
    database='db_projetoelas'
)