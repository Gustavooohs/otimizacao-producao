"""
Dashboard interativo com Plotly - 3 ABAS SEPARADAS
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def criar_dashboard(resultado, cenarios, parametros):
    """Cria 3 dashboards interativos em abas separadas"""
    
    print("🌐 Abrindo 3 dashboards em abas separadas...")
    
    # DASHBOARD 1: Comparação de Cenários
    print("📊 Criando Dashboard 1: Comparação de Cenários...")
    _criar_dashboard_cenarios(cenarios, parametros)
    
    # DASHBOARD 2: Resultado da Otimização
    print("📈 Criando Dashboard 2: Resultado da Otimização...")
    _criar_dashboard_otimizacao(resultado, parametros)
    
    # DASHBOARD 3: Análise de Sensibilidade
    print("🎛️ Criando Dashboard 3: Análise de Sensibilidade...")
    _criar_dashboard_sensibilidade(resultado, parametros)
    
    print("✅ Todos os dashboards foram abertos em abas separadas!")

def _criar_dashboard_cenarios(cenarios, parametros):
    """Dashboard 1: Comparação de Cenários"""
    
    df_cenarios = pd.DataFrame(cenarios)
    
    fig = px.bar(df_cenarios, x='nome', y='producao',
                 title='📊 DASHBOARD 1: COMPARAÇÃO DE CENÁRIOS DE PRODUÇÃO',
                 labels={'producao': 'Produção (unidades)', 'nome': 'Cenário'},
                 color='producao',
                 color_continuous_scale='Viridis',
                 text='producao')
    
    fig.update_traces(texttemplate='%{text:.0f} unidades', textposition='outside')
    fig.update_layout(showlegend=False, 
                     height=600,
                     font=dict(size=12),
                     title_font_size=18,
                     xaxis_tickangle=-45)
    
    # Adicionar linha da meta
    fig.add_hline(y=parametros['meta_diaria'], line_dash="dash", 
                  line_color="red", annotation_text="META DIÁRIA",
                  annotation_font_size=14, annotation_font_color="red")
    
    fig.show()

def _criar_dashboard_otimizacao(resultado, parametros):
    """Dashboard 2: Resultado da Otimização"""
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['🎯 Recursos Otimizados', '📈 Produção vs Meta', 
                       '💰 Custo Total', '📊 Eficiência'],
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Gráfico 1: Recursos
    fig.add_trace(
        go.Bar(name='Recursos', 
               x=['Operários', 'Horas'], 
               y=[resultado['operarios_ideais'], resultado['horas_ideais']],
               marker_color=['#2E86AB', '#A23B72'],
               text=[f'{resultado["operarios_ideais"]}', f'{resultado["horas_ideais"]:.1f}'],
               textposition='auto'),
        row=1, col=1
    )
    
    # Gráfico 2: Produção vs Meta
    fig.add_trace(
        go.Bar(name='Produção', 
               x=['Otimizada', 'Meta'], 
               y=[resultado['producao_maxima'], parametros['meta_diaria']],
               marker_color=['#F18F01', '#C73E1D'],
               text=[f'{resultado["producao_maxima"]:.0f}', f'{parametros["meta_diaria"]}'],
               textposition='auto'),
        row=1, col=2
    )
    
    # Gráfico 3: Custo
    custo_total = resultado['operarios_ideais'] * resultado['horas_ideais'] * parametros['custo_hora']
    fig.add_trace(
        go.Bar(name='Custo', 
               x=['Custo'], 
               y=[custo_total],
               marker_color=['#34A853'],
               text=[f'R$ {custo_total:.2f}'],
               textposition='outside',
               textfont=dict(size=12, color='black')),
        row=2, col=1
    )
    
    # Gráfico 4: Eficiência
    eficiencia = (resultado['producao_maxima'] / (parametros['operarios_maximos'] * parametros['horas_efetivas'] * parametros['taxa_producao'])) * 100
    fig.add_trace(
        go.Bar(name='Eficiência', 
               x=['Eficiência'], 
               y=[eficiencia],
               marker_color=['#FF6B6B'],
               text=[f'{eficiencia:.1f}%'],
               textposition='auto'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        showlegend=False,
        title_text="📋 DASHBOARD 2: RESULTADO DA OTIMIZAÇÃO",
        title_font_size=20,
        margin=dict(t=100, b=80, l=80, r=80)
    )
    
    fig.update_yaxes(title_text="Quantidade", row=1, col=1)
    fig.update_yaxes(title_text="Unidades", row=1, col=2)
    fig.update_yaxes(title_text="R$", row=2, col=1, range=[0, custo_total * 1.3])
    fig.update_yaxes(title_text="%", row=2, col=2, range=[0, 110])
    
    fig.show()

def _criar_dashboard_sensibilidade(resultado, parametros):
    """Dashboard 3: Análise de Sensibilidade 3D"""
    
    operarios = list(range(1, parametros['operarios_maximos'] + 3))
    horas = [6, 7, 8, 9, 10]
    
    producao_data = []
    for op in operarios:
        for hr in horas:
            producao = parametros['taxa_producao'] * op * hr
            custo = op * hr * parametros['custo_hora']
            eficiencia = (producao / (op * hr * parametros['taxa_producao'])) * 100
            
            producao_data.append({
                'Operarios': op,
                'Horas': hr, 
                'Producao': producao,
                'Custo': custo,
                'Eficiencia': eficiencia,
                'Status': 'Viável' if producao >= parametros['meta_diaria'] else 'Inviável'
            })
    
    df_sensibilidade = pd.DataFrame(producao_data)
    
    fig = px.scatter_3d(df_sensibilidade, 
                       x='Operarios', 
                       y='Horas', 
                       z='Producao',
                       color='Status',
                       size='Producao',
                       title='🎛️ DASHBOARD 3: ANÁLISE 3D - PRODUÇÃO vs OPERÁRIOS vs HORAS',
                       labels={'Operarios': 'Nº de Operários', 
                              'Horas': 'Horas Trabalhadas', 
                              'Producao': 'Produção (unidades)'},
                       color_discrete_map={'Viável': 'green', 'Inviável': 'red'},
                       hover_data=['Custo', 'Eficiencia'])
    
    # Adicionar plano da meta
    fig.add_trace(go.Mesh3d(
        name="Plano da Meta",
        x=[min(operarios), max(operarios), max(operarios), min(operarios)],
        y=[min(horas), min(horas), max(horas), max(horas)],
        z=[parametros['meta_diaria']] * 4,
        opacity=0.3,
        color='yellow',
        text="Meta de Produção"
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Operários',
            yaxis_title='Horas',
            zaxis_title='Produção'
        ),
        height=700,
        title_font_size=16
    )
    
    fig.show()