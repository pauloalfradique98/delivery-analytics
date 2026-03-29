from app.database.connection import get_db_connection


def get_bairros():
    conn = get_db_connection()
    bairros = conn.execute('SELECT * FROM bairros ORDER BY taxa ASC').fetchall()
    conn.close()
    return bairros


def add_bairro(nome, taxa):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO bairros (nome, taxa) VALUES (?, ?)',
        (nome, taxa)
    )
    conn.commit()
    conn.close()

def get_bairro_by_id(id):
    conn = get_db_connection()
    bairro = conn.execute(
        'SELECT * FROM bairros WHERE id = ?',
        (id,)
    ).fetchone()
    conn.close()
    return bairro


def update_bairro(id, nome, taxa):
    conn = get_db_connection()
    conn.execute(
        'UPDATE bairros SET nome = ?, taxa = ? WHERE id = ?',
        (nome, taxa, id)
    )
    conn.commit()
    conn.close()

def delete_bairro(id):
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM bairros WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()

def bairro_tem_entregas(bairro_id):
    conn = get_db_connection()
    # Conta quantas entregas existem para este bairro
    resultado = conn.execute(
        'SELECT COUNT(*) FROM deliveries WHERE bairro_id = ?', 
        (bairro_id,)
    ).fetchone()
    conn.close()
    return resultado[0] > 0