import sqlite3

con = sqlite3.connect('contratos_publicos.db')
cur = con.cursor()
cur.execute("DELETE FROM entidades;")

table = "entidades"

# Resetar o contador do auto incremento (reseta o valor para 1)
cur.execute("DELETE FROM sqlite_sequence WHERE name=?;", (table,))

con.commit()
cur.close()
con.close()