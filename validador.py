from datetime import datetime

def validar_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Data inválida! Use o formato AAAA-MM-DD.")

def validar_texto(campo, nome_campo):
    campo = campo.strip()  # ✅ Correto: chamada da função strip()
    if not campo:
        raise ValueError(f"{nome_campo} não pode estar vazio.")
    return campo

def validar_valor(valor_str):
    try:
        valor = float(valor_str)
        if valor <= 0:
            raise ValueError
        return valor
    except ValueError:
        raise ValueError("Valor deve ser um número positivo.")

def validar_parcelas(parcela_str):
    try:
        qtd = int(parcela_str)
        if qtd < 1:
            raise ValueError
        return qtd
    except ValueError:
        raise ValueError("Quantidade de parcelas deve ser um número inteiro positivo.")

def buscar_id(cursor, tabela, nome):
    cursor.execute(f"SELECT id FROM {tabela} WHERE nome = %s", (nome,))
    resultado = cursor.fetchone()
    if not resultado:
        raise ValueError(f"{tabela.capitalize()} '{nome}' não encontrada.")
    return resultado[0]

def listar_tabela(cursor, tabela):
    cursor.execute(f"SELECT id, nome FROM {tabela}")
    print(f"\n{tabela.capitalize()} disponíveis:")
    for id_, nome in cursor.fetchall():
        print(f"- ID {id_}: {nome}")
