"""
Parâmetros do problema de otimização de produção
"""

PARAMETROS = {
    'taxa_producao': 100,      # unidades/hora/operário
    'horas_maximas': 8,        # horas totais do turno
    'horas_efetivas': 7,       # horas úteis (descontando pausas)
    'operarios_maximos': 6,    # número máximo de operários
    'meta_diaria': 3000,       # meta de produção
    'custo_hora': 18.00        # R$/hora por operário
}

def mostrar_parametros():
    """Exibe os parâmetros atuais do problema"""
    print("📊 PARÂMETROS DO PROBLEMA:")
    for key, value in PARAMETROS.items():
        print(f"  {key}: {value}")