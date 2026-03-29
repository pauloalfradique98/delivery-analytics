from flask import Blueprint, render_template, request, redirect, url_for
from app.repository.delivery_repository import (
    get_historico_filtrado, 
    delete_delivery, 
    get_delivery_by_id, 
    update_delivery
)
from app.repository.bairro_repository import get_bairros
from app.services.analytics_service import montar_filtros_historico

historico_bp = Blueprint('historico', __name__)


@historico_bp.route('/historico')
def historico():
    filtros = montar_filtros_historico(request.args)

    deliveries = get_historico_filtrado(filtros)
    bairros = get_bairros()

    return render_template(
        'historico.html',
        deliveries=deliveries,
        bairros=bairros,
        filtros=request.args
    )

@historico_bp.route('/delete/<int:id>', methods=['POST'])
def delete_delivery_route(id):
    delete_delivery(id)
    return redirect(url_for('historico.historico'))

@historico_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_delivery_route(id):
    if request.method == 'POST':
        bairro_id = request.form['bairro_id']
        valor = request.form['valor']
        data = request.form['data']
        hora = request.form['hora']

        update_delivery(id, bairro_id, valor, data, hora)
        
        return redirect(url_for('historico.historico'))

    delivery = get_delivery_by_id(id)
    bairros = get_bairros()
    return render_template('edit.html', delivery=delivery, bairros=bairros)