from collections import Counter
from datetime import datetime

def calcular_kpis(deliveries):
    total_produtos = sum(d['valor_produto'] for d in deliveries)
    total_taxas = sum(d['taxa'] for d in deliveries)
    total_geral = total_produtos + total_taxas
    quantidade = len(deliveries)
    ticket_medio = total_geral / quantidade if quantidade else 0

    return {
        "total_produtos": total_produtos,
        "total_taxas": total_taxas,
        "total_geral": total_geral,
        "quantidade": quantidade,
        "ticket_medio": ticket_medio
    }

def gerar_grafico_horarios(deliveries):
    horarios_map = {}
    for d in deliveries:
        hora_str = d['hora'][:2]
        horarios_map[hora_str] = horarios_map.get(hora_str, 0) + 1

    horas_ordenadas = sorted(horarios_map.keys(), key=lambda x: int(x))
    return [f"{h}:00" for h in horas_ordenadas], [horarios_map[h] for h in horas_ordenadas]

def gerar_ranking_bairros(deliveries):
    bairros = {}
    for d in deliveries:
        nome = d['bairro']
        if nome not in bairros:
            bairros[nome] = {"quantidade": 0, "total": 0}
        bairros[nome]["quantidade"] += 1
        bairros[nome]["total"] += d['valor_produto'] + d['taxa']

    ranking = sorted(bairros.items(), key=lambda x: x[1]["quantidade"], reverse=True)
    return [b[0] for b in ranking], [b[1]["quantidade"] for b in ranking]

def gerar_grafico_semanal(deliveries):
    dias_semana_map = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'}
    contagem = { 'Seg': 0, 'Ter': 0, 'Qua': 0, 'Qui': 0, 'Sex': 0, 'Sáb': 0, 'Dom': 0 }

    for d in deliveries:
        try:
            data_obj = datetime.strptime(d['data'], '%Y-%m-%d')
            nome_dia = dias_semana_map[data_obj.weekday()]
            contagem[nome_dia] += 1
        except:
            continue
    return list(contagem.keys()), list(contagem.values())

def gerar_insights(deliveries, kpis):
    insights = []

    if not deliveries:
        return insights

    # Melhor bairro
    bairros = Counter(d['bairro'] for d in deliveries)

    if bairros:
        bairro_top = max(bairros, key=bairros.get)
        insights.append(f"🏆 Bairro com mais pedidos: {bairro_top} ({bairros[bairro_top]} entregas)")

    # Melhor horário
    horarios = {}
    for d in deliveries:
        hora = d['hora'][:2]
        horarios[hora] = horarios.get(hora, 0) + 1

    hora_top = max(horarios, key=horarios.get)
    insights.append(f"⏰ Horário mais movimentado: {hora_top}h ({horarios[hora_top]} pedidos)")

    # Melhor dia
    dias = {}
    for d in deliveries:
        dia = d['data']
        dias[dia] = dias.get(dia, 0) + 1

    dia_top = max(dias, key=dias.get)
    insights.append(f"📅 Dia com mais entregas: {dia_top} ({dias[dia_top]} pedidos)")

    # Regras inteligentes
    if kpis["ticket_medio"] > 100:
        insights.append("💰 Ticket médio alto — clientes comprando bem")
    elif kpis["ticket_medio"] < 50:
        insights.append("⚠️ Ticket médio baixo — oportunidade de aumentar valor")

    if kpis["quantidade"] > 15:
        insights.append("🔥 Alto volume de entregas — dia forte")
    elif kpis["quantidade"] < 5:
        insights.append("📉 Baixo volume — pode melhorar divulgação")

    return insights

def gerar_grafico_por_dia(dados_dia):
    """
    Recebe uma lista de dicionários vinda do repositório 
    (ex: [{'data': '2026-03-28', 'total': 150.0}])
    """
    if not dados_dia:
        return [], []
    # Ordena os dados por data antes de separar em listas
    dados_ordenados = sorted(dados_dia, key=lambda x: x['data'])
    
    labels = [d['data'] for d in dados_ordenados]
    valores = [d['total'] for d in dados_ordenados]
    
    return labels, valores

def montar_filtros_historico(args):
    # Essa função é necessária para processar as buscas no histórico
    from datetime import datetime, timedelta
    filtros = {}
    
    data = args.get('data')
    data_inicio = args.get('data_inicio')
    data_fim = args.get('data_fim')
    periodo = args.get('periodo')
    bairro = args.get('bairro')

    if data: filtros["data"] = data
    elif data_inicio and data_fim:
        filtros["data_inicio"] = data_inicio
        filtros["data_fim"] = data_fim
    elif periodo:
        hoje = datetime.today()
        if periodo == '7dias': inicio = (hoje - timedelta(days=7)).date()
        elif periodo == '30dias': inicio = (hoje - timedelta(days=30)).date()
        else: inicio = hoje.date()
        filtros["periodo_inicio"] = inicio

    if bairro: filtros["bairro"] = bairro
    return filtros

