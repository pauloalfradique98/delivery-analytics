from datetime import datetime, timedelta

def processar_filtros(args):
    """
    Centraliza a lógica de capturar os argumentos da URL 
    e transformar em filtros para o banco de dados.
    """
    filtros = {
        'data': args.get('data'),
        'data_inicio': args.get('data_inicio'),
        'data_fim': args.get('data_fim'),
        'periodo': args.get('periodo'),
        'bairro': args.get('bairro')
    }
    
    # Se houver período pré-definido, calcula a data de início
    if filtros['periodo']:
        hoje = datetime.today()
        if filtros['periodo'] == '7dias':
            filtros['periodo_calculado'] = (hoje - timedelta(days=7)).date()
        elif filtros['periodo'] == '30dias':
            filtros['periodo_calculado'] = (hoje - timedelta(days=30)).date()
            
    return filtros