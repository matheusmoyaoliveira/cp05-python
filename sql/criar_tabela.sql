CREATE TABLE vendas (
  id                  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nome_comprador      VARCHAR2(60)  NOT NULL,
  nome_vendedor       VARCHAR2(60)  NOT NULL,
  data_venda          DATE          NOT NULL,
  descricao_produtos  VARCHAR2(200) NOT NULL,
  valor_total         NUMBER(10,2)  NOT NULL,
  valor_impostos      NUMBER(10,2)  NOT NULL,
  CONSTRAINT vendas_ck_valores
    CHECK (valor_total >= 0 AND valor_impostos >= 0 AND valor_impostos <= valor_total)
);