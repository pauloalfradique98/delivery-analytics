from datetime import datetime, timedelta

def get_periodo_datas(periodo, data_inicio=None, data_fim=None):
    hoje = datetime.today()

    if data_inicio and data_fim:
        return data_inicio, data_fim

    if periodo == '7dias':
        return (hoje - timedelta(days=7)).date(), hoje.date()

    elif periodo == '30dias':
        return (hoje - timedelta(days=30)).date(), hoje.date()

    return hoje.date(), hoje.date()