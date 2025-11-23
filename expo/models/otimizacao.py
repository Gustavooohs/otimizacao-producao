"""
Modelo de otimização de produção usando Programação Linear
VERSÃO CORRIGIDA - Sem multiplicação de variáveis
"""

import pulp
import numpy as np

class OtimizadorProducao:
    def __init__(self, parametros):
        self.parametros = parametros
        
    def otimizar_producao(self):
        """Otimiza a produção usando horas fixas - MÉTODO PRINCIPAL"""
        
        prob = pulp.LpProblem("Maximizar_Producao", pulp.LpMaximize)
        
        # Variável: número de operários
        operarios = pulp.LpVariable('Operarios', lowBound=0, 
                                  upBound=self.parametros['operarios_maximos'], 
                                  cat='Integer')
        
        # Horas são fixas (usamos as horas efetivas disponíveis)
        horas_fixas = self.parametros['horas_efetivas']
        
        # Função objetivo: Maximizar produção (agora é linear)
        producao_total = self.parametros['taxa_producao'] * operarios * horas_fixas
        prob += producao_total, "Producao_Total"
        
        # Restrição: Produção deve atender meta mínima
        prob += producao_total >= self.parametros['meta_diaria'], "Meta_Minima"
        
        # Resolver o problema
        prob.solve()
        
        # Coletar resultados
        resultado = {
            'operarios_ideais': pulp.value(operarios),
            'horas_ideais': horas_fixas,
            'producao_maxima': pulp.value(producao_total),
            'meta_atingida': pulp.value(producao_total) >= self.parametros['meta_diaria'],
            'status': pulp.LpStatus[prob.status],
            'metodo': 'horas_fixas'
        }
        
        return resultado
    
    def otimizar_com_horas_variaveis(self):
        """Alternativa: Usar diferentes combinações de horas discretas"""
        
        melhor_resultado = None
        melhor_producao = 0
        
        # Testar diferentes horas discretas
        for horas in [6, 7, 8, 9]:
            prob = pulp.LpProblem(f"Maximizar_Producao_{horas}h", pulp.LpMaximize)
            
            operarios = pulp.LpVariable('Operarios', lowBound=0, 
                                      upBound=self.parametros['operarios_maximos'], 
                                      cat='Integer')
            
            # Produção com horas fixas para esta iteração
            producao_total = self.parametros['taxa_producao'] * operarios * horas
            prob += producao_total, "Producao_Total"
            
            # Restrição de meta
            prob += producao_total >= self.parametros['meta_diaria'], "Meta_Minima"
            
            # Resolver
            prob.solve()
            
            producao_atual = pulp.value(producao_total)
            
            # Encontrar a melhor combinação
            if producao_atual > melhor_producao:
                melhor_producao = producao_atual
                melhor_resultado = {
                    'operarios_ideais': pulp.value(operarios),
                    'horas_ideais': horas,
                    'producao_maxima': producao_atual,
                    'meta_atingida': producao_atual >= self.parametros['meta_diaria'],
                    'status': pulp.LpStatus[prob.status],
                    'metodo': 'horas_discretas'
                }
        
        return melhor_resultado
    
    def calcular_meta_minima(self):
        """Calcula a configuração mínima para atingir a meta"""
        
        # Operários mínimos para atingir a meta
        operarios_minimos = np.ceil(self.parametros['meta_diaria'] / 
                                  (self.parametros['taxa_producao'] * self.parametros['horas_efetivas']))
        
        return {
            'operarios_minimos': int(operarios_minimos),
            'horas_necessarias': self.parametros['horas_efetivas'],
            'producao_estimada': self.parametros['taxa_producao'] * operarios_minimos * self.parametros['horas_efetivas']
        }
    
    def calcular_custo(self, operarios, horas):
        """Calcula o custo total da produção"""
        return operarios * horas * self.parametros['custo_hora']