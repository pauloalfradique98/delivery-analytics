import sqlite3

conn = sqlite3.connect('database.db')

# Criar tabela de bairros
conn.execute('''
CREATE TABLE bairros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    taxa REAL
)
''')

# Inserir alguns bairros (exemplo)
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Costa Azul', 3.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Recreio', 5.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Colinas', 5.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Ouro Verde', 6.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Mariléia', 6.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Liberdade', 8.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Nova Esperança', 8.00)")
conn.execute("INSERT INTO bairros (nome, taxa) VALUES ('Centro', 8.00)")

conn.commit()
conn.close()