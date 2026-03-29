from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.repository.bairro_repository import get_bairros, get_bairro_by_id, add_bairro, update_bairro, delete_bairro, bairro_tem_entregas

bairros_bp = Blueprint('bairros', __name__)

@bairros_bp.route('/bairros', methods=['GET', 'POST'])
def bairros():
    if request.method == 'POST':
        nome = request.form['nome']
        taxa = request.form['taxa']
        add_bairro(nome, taxa)
        return redirect('/bairros')

    bairros = get_bairros()
    return render_template('bairros.html', bairros=bairros)

@bairros_bp.route('/edit_bairro/<int:id>', methods=['GET', 'POST'])
def edit_bairro(id):
    if request.method == 'POST':
        nome = request.form['nome']
        taxa = request.form['taxa']

        update_bairro(id, nome, taxa)
        return redirect('/bairros')

    bairro = get_bairro_by_id(id)
    return render_template('edit_bairro.html', bairro=bairro)

@bairros_bp.route('/delete_bairro/<int:id>', methods=['POST'])
def delete_bairro_route(id):
    if bairro_tem_entregas(id):
        # Aqui enviamos uma mensagem de aviso para o usuário
        flash('Não é possível excluir este bairro pois existem entregas registradas nele.', 'danger')
    else:
        delete_bairro(id)
        flash('Bairro excluído com sucesso!', 'success')
        
    return redirect(url_for('bairros.bairros'))