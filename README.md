# Checkpoint 5 – Python (Vendas com JSON)

Sistema simples de **vendas** com persistência em **JSON**, seguindo o enunciado do CP5.
Inclui DDL de banco (Oracle), scripts de carga e um roteiro de testes.

---

## 📁 Estrutura do projeto

```
checkpoint5/
├─ banco.py              # Módulo principal (funções pedidas + validações)
├─ inserir_vendas.py     # Popula o “banco” com 20 vendas de exemplo
├─ main.py               # Exercício 4: roteiro de testes das funções
├─ modelos.py            # (opcional) tipagens/auxiliares
├─ storage/
│  └─ vendas.json        # “Banco de dados” (lista de vendas)
└─ sql/
   ├─ criar_tabela.sql   # DDL da tabela VENDAS (Oracle)
   └─ apaga_tabela.sql   # Script para dropar a tabela VENDAS
```

---

## ▶️ Como executar

> Pré-requisito: Python 3.10+ (sem bibliotecas externas).

1. **Popular dados (20 vendas):**
   ```bash
   python inserir_vendas.py
   ```

2. **Executar os testes do exercício 4 (alterar/buscar/relatório):**
   ```bash
   python main.py
   ```

3. **Resetar o “banco” (caso queira recomeçar do zero):**
   - Abra `storage/vendas.json` e deixe apenas:
     ```json
     []
     ```

---

## 🧩 Funções expostas em `banco.py`

- `inclui(venda: dict) -> int`  
  Insere uma venda **nova**. Gera `id` automaticamente e salva no JSON.  
  **Validações:** campos obrigatórios, data `YYYY-MM-DD`, números ≥ 0, `impostos ≤ total`.

- `altera(venda: dict) -> None`  
  Altera campos de uma venda **existente** (obrigatório passar `id`).  
  Atualização **parcial** é suportada: apenas as chaves presentes são modificadas.

- `recupera_vendas_data(ini: str, fim: str) -> list[dict]`  
  Retorna as vendas entre `ini` e `fim` (inclusive), ordenadas por `(data_venda, id)`.

- `recupera_vendas_comprador(vendedor: str) -> list[dict]`  
  **Obs.:** apesar do nome do enunciado, o parâmetro é `vendedor`.  
  Implementado como **filtro por VENDEDOR** (case-insensitive, termo contido).

- `relatorio_vendas() -> str`  
  Gera um relatório com: quantidade total, soma de valores, soma de impostos e
  **quebra por vendedor** (ordenada por total decrescente).

### Modelo de venda (dicionário)
```python
{
  "id": int,                     # gerado automaticamente
  "nome_comprador": str,
  "nome_vendedor": str,
  "data_venda": "YYYY-MM-DD",    # string ISO
  "descricao_produtos": str,
  "valor_total": float,
  "valor_impostos": float
}
```

---

## 🧠 Decisões de projeto & validações

- Persistência em **JSON** para simular o banco (sem dependências externas).
- Datas em **ISO** para facilitar parsing e ordenação.
- Números **forçados para float** e **arredondados a 2 casas** ao salvar/alterar.
- **Erros claros**:
  - `ValueError` para entradas inválidas (campos ausentes, data inválida, valores negativos).
  - `LookupError` para “venda não encontrada” em `altera`.
- Helpers internos (`_carregar`, `_salvar`, `_proximo_id`, `_parse_data_iso`, etc.) com prefixo `_`
  como convenção de “uso interno”.

> Dica: o arquivo JSON é tolerante a corrupção — se não for possível fazer o `json.load`, o sistema considera lista vazia para não quebrar a execução do CP.

---

## 🗃️ Scripts SQL (Oracle)

- `sql/criar_tabela.sql` – cria a tabela `VENDAS`. Versão forte sugerida:

  ```sql
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
  ```

- `sql/apaga_tabela.sql` – apaga a tabela `VENDAS`. Versão robusta (não erra se a tabela não existir):
  ```sql
  BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE vendas CASCADE CONSTRAINTS PURGE';
  EXCEPTION
    WHEN OTHERS THEN
      IF SQLCODE != -942 THEN  -- ORA-00942: table or view does not exist
        RAISE;
      END IF;
  END;
  /
  ```

---

## 📝 Observações importantes

- Rodar `inserir_vendas.py` mais de uma vez **acumula** vendas (pois não limpa o JSON). Use o “reset” se quiser recomeçar.
- No `main.py`, usamos `if __name__ == "__main__":` para que o script rode apenas quando executado diretamente, e não quando o módulo é importado.

---

## ✅ Como o professor pode testar rapidamente

```bash
# 1) Popular o "banco" com 20 vendas
python inserir_vendas.py

# 2) Rodar o roteiro de testes
python main.py
```

Saída esperada: confirmação de alteração de uma venda, listagens parciais das buscas e o relatório final com totais e quebra por vendedor.
