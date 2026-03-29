from app.database.connection import get_db_connection

def add_delivery(bairro_id, valor_produto, data, hora):
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO deliveries (bairro_id, valor_produto, data, hora)
        VALUES (?, ?, ?, ?)
        ''',
        (bairro_id, valor_produto, data, hora)
    )
    conn.commit()
    conn.close()

def delete_delivery(delivery_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM deliveries WHERE id = ?",
        (delivery_id,)
    )
    conn.commit()
    conn.close()

def get_metricas_data(data_inicio, data_fim):
    conn = get_db_connection()

    deliveries = conn.execute('''
        SELECT d.valor_produto, b.taxa, d.data, d.hora, b.nome as bairro
        FROM deliveries d
        JOIN bairros b ON d.bairro_id = b.id
        WHERE d.data BETWEEN ? AND ?
    ''', (data_inicio, data_fim)).fetchall()

    conn.close()
    return deliveries

def get_entregas_por_dia(data_inicio, data_fim):
    conn = get_db_connection()

    dados = conn.execute('''
        SELECT data, COUNT(*) as total
        FROM deliveries
        WHERE data BETWEEN ? AND ?
        GROUP BY data
        ORDER BY data
    ''', (data_inicio, data_fim)).fetchall()

    conn.close()
    return dados

def get_deliveries_by_period(data_inicio, data_fim):
    conn = get_db_connection()

    deliveries = conn.execute('''
        SELECT 
            d.id,
            d.valor_produto,
            d.data,
            d.hora,
            b.nome as bairro,
            b.taxa as taxa
        FROM deliveries d
        JOIN bairros b ON d.bairro_id = b.id
        WHERE d.data BETWEEN ? AND ?
        ORDER BY d.data ASC, d.hora ASC
    ''', (data_inicio, data_fim)).fetchall()

    conn.close()
    return deliveries

def get_historico_filtrado(filtros):
    conn = get_db_connection()

    query = '''
        SELECT d.*, b.nome as bairro, b.taxa
        FROM deliveries d
        JOIN bairros b ON d.bairro_id = b.id
        WHERE 1=1
    '''

    params = []

    if filtros.get("data"):
        query += " AND d.data = ?"
        params.append(filtros["data"])

    if filtros.get("data_inicio") and filtros.get("data_fim"):
        query += " AND d.data BETWEEN ? AND ?"
        params.append(filtros["data_inicio"])
        params.append(filtros["data_fim"])

    elif filtros.get("periodo_inicio"):
        query += " AND d.data >= ?"
        params.append(filtros["periodo_inicio"])

    if filtros.get("bairro"):
        query += " AND d.bairro_id = ?"
        params.append(filtros["bairro"])

    query += " ORDER BY d.data DESC, d.hora DESC"

    deliveries = conn.execute(query, params).fetchall()
    conn.close()

    return deliveries

def update_delivery(delivery_id, bairro_id, valor_produto, data, hora):
    conn = get_db_connection()
    conn.execute(
        '''
        UPDATE deliveries 
        SET bairro_id = ?, valor_produto = ?, data = ?, hora = ?
        WHERE id = ?
        ''',
        (bairro_id, valor_produto, data, hora, delivery_id)
    )
    conn.commit()
    conn.close()

def get_delivery_by_id(delivery_id):
    conn = get_db_connection()
    delivery = conn.execute('SELECT * FROM deliveries WHERE id = ?', (delivery_id,)).fetchone()
    conn.close()
    return delivery