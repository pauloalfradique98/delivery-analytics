import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE bairros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    taxa REAL
)
''')

conn.execute('''
CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_produto REAL,
    bairro_id INTEGER,
    data TEXT,
    hora TEXT,
    FOREIGN KEY (bairro_id) REFERENCES bairros (id)
)
''')

# Dados iniciais
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