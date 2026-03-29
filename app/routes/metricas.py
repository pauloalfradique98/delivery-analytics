from flask import Blueprint, render_template, request
from app.services.analytics_service import (
    calcular_kpis,
    gerar_grafico_por_dia,
    gerar_insights
)
from app.utils.date_utils import get_periodo_datas
from app.repository.delivery_repository import (
    get_metricas_data,
    get_entregas_por_dia
)

metricas_bp = Blueprint('metricas', __name__)


@metricas_bp.route('/metricas')
def metricas():
    periodo = request.args.get('periodo')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    data_inicio, data_fim = get_periodo_datas(periodo, data_inicio, data_fim)

    deliveries = get_metricas_data(data_inicio, data_fim)
    dados_dia = get_entregas_por_dia(data_inicio, data_fim)

    kpis = calcular_kpis(deliveries)
    labels_dia, valores_dia = gerar_grafico_por_dia(dados_dia)

    insights = gerar_insights(deliveries, kpis)

    return render_template(
        'metricas.html',
        labels_dia=labels_dia,
        valores_dia=valores_dia,
        periodo=periodo,
        insights=insights,
        **kpis
    )