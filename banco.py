import json
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime, date

"""Módulo de persistência de vendas em JSON (arquivo storage/vendas.json)."""

__all__ = [
    "inclui",
    "altera",
    "recupera_vendas_data",
    "recupera_vendas_comprador",
    "relatorio_vendas",
]

_ARQ = Path(__file__).parent / "storage" / "vendas.json"

def inclui(venda: dict):

    OBRIG = ["nome_comprador","nome_vendedor","data_venda","descricao_produtos","valor_total","valor_impostos"]

    vendas = _carregar()
    _assert_campos_obrigatorios(venda, OBRIG)
    _parse_data_iso(venda["data_venda"])
    _assert_numeros(venda)
    venda["valor_total"] = round(float(venda["valor_total"]))
    venda["valor_impostos"] = round(float(venda["valor_impostos"]))
    venda["nome_comprador"] = venda["nome_comprador"].strip()
    venda["nome_vendedor"] = venda["nome_vendedor"].strip()
    venda["descricao_produtos"] = venda["descricao_produtos"].strip()
    novo_id = _proximo_id(vendas)
    reg = {
        "id": novo_id,
        "nome_comprador": venda["nome_comprador"],
        "nome_vendedor": venda["nome_vendedor"],
        "data_venda": venda["data_venda"],
        "descricao_produtos": venda["descricao_produtos"],
        "valor_total": float(venda["valor_total"]),
        "valor_impostos": float(venda["valor_impostos"]),
    }
    vendas.append(reg)
    _salvar(vendas)
    
    return novo_id

def altera(venda: dict):

    if "id" not in venda:
        raise ValueError("id obrigatório")
    vendas = _carregar()
    idx = next((i for i, x in enumerate(vendas) if x["id"] == venda["id"]), None)
    if idx == None:
        raise LookupError("venda não encontrada")
    atual = vendas[idx].copy()

    for campo in ("nome_comprador","nome_vendedor","data_venda","descricao_produtos","valor_total","valor_impostos"):
        if campo in venda:
            val = venda[campo]
            if isinstance(val, str):
                val = val.strip()
            atual[campo] = val

    _parse_data_iso(atual["data_venda"])
    _assert_campos_obrigatorios(atual, ["nome_comprador","nome_vendedor","data_venda","descricao_produtos","valor_total","valor_impostos"])
    _assert_numeros(atual)

    atual["valor_total"] = round(float(atual["valor_total"]))
    atual["valor_impostos"] = round(float(atual["valor_impostos"]))

    vendas[idx] = atual
    _salvar(vendas)

def _carregar():

    if not _ARQ.exists():
        return []
    try:
        with open(_ARQ, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except JSONDecodeError:
        return []
    return dados if isinstance(dados, list) else []

def _salvar(lista):

    with open(_ARQ, "w", encoding="utf-8") as f: 
        json.dump(lista, f, ensure_ascii=False, indent=2, sort_keys=True)

def _proximo_id(lista):

    return 1 if not lista else max(v.get("id", 0) for v in lista) + 1

def _parse_data_iso(s: str) -> date:

    return datetime.strptime(s, "%Y-%m-%d").date()

def _assert_numeros(v: dict):
    try:
        total = float(v["valor_total"])
        imp = float (v["valor_impostos"])
    except Exception:
        raise ValueError("Valores numéricos inválidos (total/impostos)")
    
    if total < 0 or imp < 0:
        raise ValueError("Valores não podem ser negativos")
    if imp > total:
        raise ValueError("Impostos não podem ser maiores que o total")

def _assert_campos_obrigatorios(v, chaves):

    for chave in chaves:
        if not chave in v:
            raise ValueError(f"Campo obrigatório ausente: {chave}")
        val = v[chave]
        if isinstance(val, str) and val.strip() == "":
            raise ValueError(f"Campo '{chave}' não pode ser vazio")
        
def recupera_vendas_comprador(vendedor: str):
    """Retorna as vendas cuja data_venda está entre [ini, fim] (inclusive).
    Parâmetros:
      ini, fim: strings ISO 'YYYY-MM-DD'.
    Retorno:
      list[dict] ordenada por (data_venda, id).
    Levanta:
      ValueError se ini/fim estiverem em formato inválido.
    """

    term = vendedor.strip().casefold()
    if not term:
        return []
    
    vendas = _carregar()

    filtradas = []
    for v in vendas:
        nome = v["nome_vendedor"].casefold()

        if term in nome:
            filtradas.append(v) 
    
    filtradas.sort(key=lambda v: (v["data_venda"], v["id"]))

    return filtradas

def recupera_vendas_data(ini: str, fim: str) -> list:
    dini = _parse_data_iso(ini)
    dfim = _parse_data_iso(fim)

    if dini > dfim:
        dini, dfim = dfim, dini

    vendas = _carregar() 

    filtradas = []
    for v in vendas:
        dv = _parse_data_iso(v["data_venda"])
        if dini <= dv <= dfim:
            filtradas.append(v)

    filtradas.sort(key=lambda v: (v["data_venda"], v["id"]))

    return filtradas

def relatorio_vendas():
    vendas = _carregar()
    qtd = len(vendas)
    soma_total = sum(float(v["valor_total"]) for v in vendas)
    soma_imp = sum(float(v["valor_impostos"]) for v in vendas)

    por_vend = {}
    for v in vendas:
        nome = v["nome_vendedor"]
        stats = por_vend.setdefault(nome, {"qtd": 0, "total": 0.0, "imp": 0.0})
        stats["qtd"] += 1
        stats["total"] += float(v["valor_total"])
        stats["imp"] += float(v["valor_impostos"])

    linhas = []
    linhas.append("RELATÓRIO DE VENDAS")
    linhas.append("-" * 20)
    linhas.append(f"Quantidade: {qtd}")
    linhas.append(f"Soma Total: {_fmt(soma_total)}")
    linhas.append(f"Impostos:   {_fmt(soma_imp)}")

    if por_vend:
        linhas.append("")
        linhas.append("Por Vendedor:")

        ordenado = sorted(
            por_vend.items(),
            key=lambda kv: kv[1]["total"],
            reverse=True
        )

        for nome, stats in ordenado:
            linhas.append(
                f"- {nome:<12} | qtd {stats['qtd']:>2} | "
                f"total {_fmt(stats['total'])} | imp {_fmt(stats['imp'])}"
            )

        return "\n".join(linhas)

def _fmt(v):
    return f"R$ {float(v):.2f}"
        