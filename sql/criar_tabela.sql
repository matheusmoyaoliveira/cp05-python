CREATE TABLE vendas (
    id number generated always as identity,
    nome_comprador varchar2(20),
    nome_vendedor varchar2(30),
    data_venda date,
    descricao_produtos varchar2(150),
    valor_total number,
    valor_impostos number
)