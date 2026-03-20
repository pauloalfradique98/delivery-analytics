from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    hoje = date.today().isoformat()

    # Buscar dados
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
    WHERE d.data = ?
    ''', (hoje,)).fetchall()

    bairros = conn.execute('SELECT * FROM bairros').fetchall()

    # Cálculos
    total_produtos = sum([d['valor_produto'] for d in deliveries]) if deliveries else 0
    total_taxas = sum([d['taxa'] for d in deliveries]) if deliveries else 0
    total_geral = total_produtos + total_taxas

    quantidade = len(deliveries)
    ticket_medio = total_geral / quantidade if quantidade > 0 else 0

    # Análise (usa deliveries já criado)
    horarios = {}

    for d in deliveries:
        hora = d['hora'][:2]

        if hora not in horarios:
            horarios[hora] = 0

        horarios[hora] += 1

    bairros_ranking = {}

    for d in deliveries:
        bairro = d['bairro']

        if bairro not in bairros_ranking:
            bairros_ranking[bairro] = {
                'quantidade': 0,
                'total_produto': 0,
                'total_geral': 0
            }

        bairros_ranking[bairro]['quantidade'] += 1
        bairros_ranking[bairro]['total_produto'] += d['valor_produto']
        bairros_ranking[bairro]['total_geral'] += d['valor_produto'] + d['taxa']

    ranking_ordenado = sorted(
        bairros_ranking.items(),
        key=lambda x: x[1]['total_geral'],
        reverse=True
    )

    # HORÁRIOS
    horas_labels = list(horarios.keys())
    horas_valores = list(horarios.values())

    # BAIRROS
    bairros_labels = [b[0] for b in ranking_ordenado]
    bairros_valores = [b[1]['quantidade'] for b in ranking_ordenado]
    conn.close()

    # Enviar pro HTML
    return render_template(
        'index.html',
        deliveries=deliveries,
        bairros=bairros,
        total_produtos=total_produtos,
        total_taxas=total_taxas,
        total_geral=total_geral,
        quantidade=quantidade,
        ticket_medio=ticket_medio,
        horarios=horarios,
        ranking_ordenado=ranking_ordenado,
        horas_labels=horas_labels,
        horas_valores=horas_valores,
        bairros_labels=bairros_labels,
        bairros_valores=bairros_valores
    )

@app.route('/metricas')
def metricas():
    conn = get_db_connection()

    periodo = request.args.get('periodo', 'hoje')

    hoje = datetime.today()

    if periodo == '7dias':
        data_inicio = (hoje - timedelta(days=7)).date()
    elif periodo == '30dias':
        data_inicio = (hoje - timedelta(days=30)).date()
    else:
        data_inicio = hoje.date()

    # FILTRO NO BANCO
    deliveries = conn.execute('''
        SELECT d.valor_produto, b.taxa, d.data
        FROM deliveries d
        JOIN bairros b ON d.bairro_id = b.id
        WHERE d.data >= ?
    ''', (data_inicio,)).fetchall()

    total_produtos = sum([d['valor_produto'] for d in deliveries])
    total_taxas = sum([d['taxa'] for d in deliveries])
    total_geral = total_produtos + total_taxas

    quantidade = len(deliveries)
    ticket_medio = total_geral / quantidade if quantidade > 0 else 0

    # GRÁFICO
    dados_dia = conn.execute('''
        SELECT data, COUNT(*) as total
        FROM deliveries
        WHERE data >= ?
        GROUP BY data
        ORDER BY data
    ''', (data_inicio,)).fetchall()

    labels_dia = [d["data"] for d in dados_dia]
    valores_dia = [d["total"] for d in dados_dia]

    conn.close()

    return render_template(
        'metricas.html',
        total_produtos=total_produtos,
        total_taxas=total_taxas,
        total_geral=total_geral,
        ticket_medio=ticket_medio,
        labels_dia=labels_dia,
        valores_dia=valores_dia,
        periodo=periodo
    )

@app.route('/add', methods=['POST'])
def add_delivery():
    valor_produto = request.form['valor']
    bairro_id = request.form['bairro_id']
    data = request.form['data']
    hora = request.form['hora']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO deliveries (valor_produto, bairro_id, data, hora) VALUES (?, ?, ?, ?)',
        (valor_produto, bairro_id, data, hora)
    )
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/historico', methods=['GET', 'POST'])
def historico():
    conn = get_db_connection()

    data_filtro = None
    deliveries = []

    if request.method == 'POST':
        data_filtro = request.form['data']

        deliveries = conn.execute('''
            SELECT d.*, b.nome as bairro, b.taxa
            FROM deliveries d
            JOIN bairros b ON d.bairro_id = b.id
            WHERE d.data = ?
        ''', (data_filtro,)).fetchall()

    conn.close()

    return render_template(
        'historico.html',
        deliveries=deliveries,
        data_filtro=data_filtro
    )

if __name__ == '__main__':
    app.run(debug=True)