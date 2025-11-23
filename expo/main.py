"""
Projeto de Otimização de Produção
Sistema de decisão para maximizar produção em fábrica de engrenagens
"""

from data.parametros import PARAMETROS, mostrar_parametros
from models.otimizacao import OtimizadorProducao
from models.simulacao import SimuladorCenarios
from visualization.dashboard import criar_dashboard

def main():
    print("🏭 SISTEMA DE OTIMIZAÇÃO DE PRODUÇÃO")
    print("=" * 50)
    
    # Mostrar parâmetros
    mostrar_parametros()
    
    # Otimização principal
    print("\n🔧 OTIMIZANDO PRODUÇÃO...")
    otimizador = OtimizadorProducao(PARAMETROS)
    resultado = otimizador.otimizar_producao()
    
    # Mostrar resultados
    print("\n📈 RESULTADO DA OTIMIZAÇÃO:")
    print(f"Operários ideais: {resultado['operarios_ideais']}")
    print(f"Horas ideais: {resultado['horas_ideais']:.2f}")
    print(f"Produção máxima: {resultado['producao_maxima']:.0f} unidades")
    print(f"Meta atingida: {'✅ SIM' if resultado['meta_atingida'] else '❌ NÃO'}")
    print(f"Status: {resultado['status']}")
    
    # Calcular custo
    custo = otimizador.calcular_custo(resultado['operarios_ideais'], resultado['horas_ideais'])
    print(f"Custo total: R$ {custo:.2f}")
    
    # Método alternativo
    print("\n🔄 TESTANDO MÉTODO ALTERNATIVO...")
    resultado_alternativo = otimizador.otimizar_com_horas_variaveis()
    
    if resultado_alternativo:
        print(f"Melhor cenário alternativo: {resultado_alternativo['producao_maxima']:.0f} unidades")
    
    # Cálculo da meta mínima
    meta_minima = otimizador.calcular_meta_minima()
    print(f"Operários mínimos para meta: {meta_minima['operarios_minimos']}")
    
    # Simular cenários
    print("\n🔄 SIMULANDO CENÁRIOS...")
    simulador = SimuladorCenarios(PARAMETROS)
    cenarios = simulador.simular_cenarios()
    
    print("\n📊 COMPARAÇÃO DE CENÁRIOS:")
    for cenario in cenarios:
        print(f"  {cenario['nome']}: {cenario['producao']:.0f} unidades")
    
    # DASHBOARD INTERATIVO UNIFICADO
    print("\n📱 CRIANDO DASHBOARD INTERATIVO UNIFICADO...")
    try:
        criar_dashboard(resultado, cenarios, PARAMETROS)
        print("✅ Dashboard interativo criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no dashboard: {e}")
    
    print("\n" + "=" * 50)
    print("✅ PROJETO CONCLUÍDO COM SUCESSO!")
    print("🌐 Dashboard interativo aberto no navegador")
    print("=" * 50)

if __name__ == "__main__":
    main()