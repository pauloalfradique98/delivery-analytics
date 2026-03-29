from flask import Blueprint, render_template, redirect, request, url_for
from datetime import date
from app.repository.delivery_repository import add_delivery, delete_delivery, get_deliveries_by_period, get_delivery_by_id, update_delivery
from app.repository.bairro_repository import get_bairros
from app.utils.date_utils import get_periodo_datas
from app.services.analytics_service import (
    calcular_kpis,
    gerar_grafico_horarios,
    gerar_grafico_semanal,
    gerar_ranking_bairros
)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    periodo = request.args.get('periodo', 'hoje')

    data_inicio, data_fim = get_periodo_datas(periodo)

    deliveries = get_deliveries_by_period(data_inicio, data_fim)
    bairros = get_bairros()

    kpis = calcular_kpis(deliveries)

    horas_labels, horas_valores = gerar_grafico_horarios(deliveries)
    semana_labels, semana_valores = gerar_grafico_semanal(deliveries)
    bairros_labels, bairros_valores = gerar_ranking_bairros(deliveries)

    return render_template(
        'index.html',
        deliveries=deliveries,
        bairros=bairros,
        horas_labels=horas_labels,
        horas_valores=horas_valores,
        semana_labels=semana_labels,
        semana_valores=semana_valores,
        bairros_labels=bairros_labels,
        bairros_valores=bairros_valores,
        periodo=periodo,
        hoje=date.today().isoformat(),
        **kpis
    )

@dashboard_bp.route('/add', methods=['POST'])
def add_delivery_route():

    valor = float(request.form['valor'])
    bairro_id = int(request.form['bairro_id'])
    data = request.form['data']
    hora = request.form['hora']

    add_delivery(bairro_id, valor, data, hora)

    return redirect('/')

@dashboard_bp.route('/delete/<int:id>')
def delete_delivery_route(id):
    delete_delivery(id)
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route("/edit/<int:id>", methods=["GET"])
def edit_delivery_page(id):
    delivery = get_delivery_by_id(id)
    bairros = get_bairros()

    return render_template("edit.html", delivery=delivery, bairros=bairros)