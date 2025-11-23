"""
Criação de gráficos estáticos com Matplotlib e Seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizador:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def criar_graficos(self, resultado, cenarios):
        """Cria todos os gráficos estáticos"""
        
        print("📈 Gerando gráficos...")
        
        # Gráfico 1: Cenários
        self._grafico_producao_cenarios(cenarios)
        print("✅ Gráfico de cenários salvo como 'grafico_cenarios.png'")
        
        # Gráfico 2: Otimização
        self._grafico_otimizacao(resultado)
        print("✅ Gráfico de otimização salvo como 'grafico_otimizacao.png'")
        
        # Gráfico 3: Sensibilidade
        self._grafico_sensibilidade()
        print("✅ Gráfico de sensibilidade salvo como 'grafico_sensibilidade.png'")
        
        print("🎨 Todos os gráficos foram gerados e salvos!")
        
    def _grafico_producao_cenarios(self, cenarios):
        """Gráfico de barras comparando cenários"""
        
        df_cenarios = pd.DataFrame(cenarios)
        
        plt.figure(figsize=(12, 7))
        bars = plt.bar(df_cenarios['nome'], df_cenarios['producao'], 
                      color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'],
                      alpha=0.8)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{height:.0f} unidades', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Comparação de Produção por Cenário', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Produção (unidades)', fontsize=12)
        plt.xlabel('Cenários', fontsize=12)
        plt.xticks(rotation=15)
        plt.grid(axis='y', alpha=0.3)
        
        # Adicionar linha da meta
        plt.axhline(y=3000, color='red', linestyle='--', linewidth=2, label='Meta (3000 unidades)')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('grafico_cenarios.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def _grafico_otimizacao(self, resultado):
        """Gráfico do resultado da otimização"""
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Gráfico 1: Recursos otimizados
        recursos = ['Operários', 'Horas']
        valores = [resultado['operarios_ideais'], resultado['horas_ideais']]
        cores = ['#2E86AB', '#A23B72']
        
        bars1 = ax1.bar(recursos, valores, color=cores, alpha=0.8)
        ax1.set_title('Recursos Otimizados', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Quantidade', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Produção vs Meta
        producao_meta = [resultado['producao_maxima'], 3000]
        labels = ['Produção\nOtimizada', 'Meta\nDiária']
        cores2 = ['#F18F01', '#C73E1D']
        
        bars2 = ax2.bar(labels, producao_meta, color=cores2, alpha=0.8)
        ax2.set_title('Produção vs Meta', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Unidades', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 3: Custo
        custo = resultado['operarios_ideais'] * resultado['horas_ideais'] * 18
        ax3.bar(['Custo Total'], [custo], color='#34A853', alpha=0.8)
        ax3.set_title('Custo de Produção', fontweight='bold', fontsize=14)
        ax3.set_ylabel('R$', fontsize=12)
        ax3.grid(axis='y', alpha=0.3)
        ax3.text(0, custo + 20, f'R$ {custo:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('grafico_otimizacao.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def _grafico_sensibilidade(self):
        """Gráfico de sensibilidade da produção"""
        
        operarios_range = range(1, 9)
        horas_range = [6, 7, 8, 9]
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        for i, horas in enumerate(horas_range):
            producao = [100 * op * horas for op in operarios_range]
            ax.plot(operarios_range, producao, marker='o', 
                   label=f'{horas} horas', linewidth=3, markersize=8, color=cores[i])
        
        # Linha da meta
        ax.axhline(y=3000, color='red', linestyle='--', linewidth=3, 
                  label='Meta (3000 unidades)', alpha=0.8)
        
        # Área viável
        ax.axvspan(5, 8, alpha=0.2, color='green', label='Zona Viável (≥ Meta)')
        
        ax.set_xlabel('Número de Operários', fontsize=12)
        ax.set_ylabel('Produção (unidades)', fontsize=12)
        ax.set_title('Sensibilidade: Produção vs Operários e Horas', 
                    fontweight='bold', fontsize=16, pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Adicionar anotações
        ax.annotate('Mínimo: 5 operários\ncom 7 horas', 
                   xy=(5, 3500), xytext=(3, 4500),
                   arrowprops=dict(arrowstyle='->', color='black'),
                   fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        plt.tight_layout()
        plt.savefig('grafico_sensibilidade.png', dpi=300, bbox_inches='tight')
        plt.show()