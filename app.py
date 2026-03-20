from datetime import date
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
        ranking_ordenado=ranking_ordenado
    )

@app.route('/metricas')
def metricas():
    conn = get_db_connection()

    deliveries = conn.execute('''
        SELECT d.valor_produto, b.taxa
        FROM deliveries d
        JOIN bairros b ON d.bairro_id = b.id
    ''').fetchall()

    total_produtos = sum([d['valor_produto'] for d in deliveries])
    total_taxas = sum([d['taxa'] for d in deliveries])
    total_geral = total_produtos + total_taxas

    quantidade = len(deliveries)
    ticket_medio = total_produtos / quantidade if quantidade > 0 else 0

    conn.close()

    return render_template(
        'metricas.html',
        total_produtos=total_produtos,
        total_taxas=total_taxas,
        total_geral=total_geral,
        ticket_medio=ticket_medio
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

if __name__ == '__main__':
    app.run(debug=True)