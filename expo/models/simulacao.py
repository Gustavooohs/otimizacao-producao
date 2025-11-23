"""
Simulação de diferentes cenários de produção
"""

import numpy as np

class SimuladorCenarios:
    def __init__(self, parametros):
        self.parametros = parametros
        
    def simular_cenarios(self):
        """Simula diferentes cenários de produção"""
        
        cenarios = []
        
        # Cenário 1: Configuração atual
        cenarios.append({
            'nome': 'Cenário Atual',
            'operarios': self.parametros['operarios_maximos'],
            'horas': self.parametros['horas_efetivas'],
            'producao': self.parametros['taxa_producao'] * self.parametros['operarios_maximos'] * self.parametros['horas_efetivas']
        })
        
        # Cenário 2: Com hora extra
        cenarios.append({
            'nome': 'Hora Extra (9h)',
            'operarios': self.parametros['operarios_maximos'],
            'horas': 9,
            'producao': self.parametros['taxa_producao'] * self.parametros['operarios_maximos'] * 9
        })
        
        # Cenário 3: Mais operários
        cenarios.append({
            'nome': 'Mais Operários (8)',
            'operarios': 8,
            'horas': self.parametros['horas_efetivas'],
            'producao': self.parametros['taxa_producao'] * 8 * self.parametros['horas_efetivas']
        })
        
        # Cenário 4: Maior produtividade
        cenarios.append({
            'nome': 'Produtividade +20%',
            'operarios': self.parametros['operarios_maximos'],
            'horas': self.parametros['horas_efetivas'],
            'producao': 120 * self.parametros['operarios_maximos'] * self.parametros['horas_efetivas']
        })
        
        return cenarios