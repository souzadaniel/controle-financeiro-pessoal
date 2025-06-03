import pandas as pd
import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='orcamento_financeiro'
)

query = '''
SELECT 
    l.id AS lancamento_id, 
    l.data AS data_lancamento, 
    l.descricao, 
    l.valor, 
    c.nome AS categoria,
    c.tipo AS tipo_categoria,
    l.tipo_lancamento,
    l.fixo,
    l.parcelado,
    l.qtd_parcelas,
    ct.nome AS conta,
    n.nome AS natureza,
    p.numero AS numero_parcela,
    p.data AS data_parcela,
    p.valor AS valor_parcela
FROM lancamentos l
JOIN categorias c ON l.categoria_id = c.id
JOIN contas ct ON l.conta_id = ct.id
JOIN naturezas n ON c.natureza_id = n.id
LEFT JOIN parcelas p ON l.id = p.lancamento_id
ORDER BY l.data DESC, p.numero;
'''

df = pd.read_sql(query, conexao)
print(df)

conexao.close()