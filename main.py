from banco import (
    altera,
    recupera_vendas_data,
    recupera_vendas_comprador,
    relatorio_vendas,
)

if __name__ == "__main__":

    atualizacao = {
        "id": 1,
        "descricao_produtos": "Notebook Gamer",
        "valor_total": 4500.00,
        "valor_impostos": 450.00,
    }
    altera(atualizacao)
    print("A) Venda 1 alterada com sucesso.\n")

    vendas_periodo = recupera_vendas_data("2025-09-10", "2025-09-20")
    print(f"B) Vendas entre 10 e 20/09: {len(vendas_periodo)} registros")

    for v in vendas_periodo[:3]:
        print(f"   - {v['data_venda']} | id {v['id']} | {v['nome_vendedor']} -> {v['nome_comprador']} | R$ {v['valor_total']:.2f}")
    print()

    vendas_vendedor = recupera_vendas_comprador("Edu")
    print(f"C) Vendas do vendedor 'Edu*': {len(vendas_vendedor)} registros")
    for v in vendas_vendedor[:3]:
        print(f"   - {v['data_venda']} | id {v['id']} | {v['nome_vendedor']} -> {v['nome_comprador']} | R$ {v['valor_total']:.2f}")
    print()

    print("D) Relatório de Vendas")
    print(relatorio_vendas())