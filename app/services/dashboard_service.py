from app.services import analytics_service

def calcular_dashboard(deliveries):
    # Chama o motor para calcular o básico
    kpis = analytics_service.calcular_kpis(deliveries)
    
    # Chama o motor para os gráficos
    h_labels, h_valores = analytics_service.gerar_grafico_horarios(deliveries)
    b_labels, b_valores = analytics_service.gerar_ranking_bairros(deliveries)
    s_labels, s_valores = analytics_service.gerar_grafico_semanal(deliveries) # Nova métrica!

    # Une tudo em um dicionário para a rota
    return {
        **kpis,
        'horas_labels': h_labels,
        'horas_valores': h_valores,
        'bairros_labels': b_labels,
        'bairros_valores': b_valores,
        'semana_labels': s_labels,
        'semana_valores': s_valores
    }