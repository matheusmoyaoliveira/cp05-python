from banco import inclui
from datetime import date, timedelta
from random import choice, randint, uniform, seed

seed(42)

inicio = date(2025, 9, 1)
def data_aleatoria():
    return (inicio + timedelta(days=randint(0, 40))).isoformat()

compradores = ["Matheus", "Ana", "João", "Beatriz", "Carlos", "Maria", "Pedro", "Luiza"]
vendedores  = ["Eduardo", "Beatriz", "Carla", "Rafael", "Helena", "Gustavo"]
descricoes  = ["Notebook", "Teclado + Mouse", "Monitor 27\"", "Headset", "SSD 1TB", "Cadeira gamer", "Webcam"]

def inserir_vendas():
    for _ in range(20):
        nome_comprador = choice(compradores)
        nome_vendedor = choice(vendedores)
        data_venda = data_aleatoria()
        descricao = choice(descricoes)

        valor_total = round(uniform(50, 3000), 2)
        valor_impostos = round(valor_total * 0.10, 2)

        venda = {
            "nome_comprador":   nome_comprador,
            "nome_vendedor":    nome_vendedor,
            "data_venda":       data_venda,
            "descricao_produtos": descricao,
            "valor_total":      valor_total,
            "valor_impostos":   valor_impostos,
        }

        novo_id = inclui(venda)
        print(f"Inserida venda {novo_id}: {nome_vendedor} → {nome_comprador} | {descricao} | {data_venda} | R$ {valor_total:.2f}")

if __name__ == "__main__":
    inserir_vendas()
    print("OK, 20 vendas inseridas.")