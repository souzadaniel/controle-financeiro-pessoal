import os  #
from conexao import conectar
from validador import (
    validar_data,
    validar_valor,
    validar_texto,
    listar_tabela,
    buscar_id
)

def inserir_lancamento():
    while True:
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            data = validar_data(input("Data do lançamento (AAAA-MM-DD): "))
            descricao = validar_texto(input("Descrição: "), "Descrição")
            valor_total = validar_valor(input("Valor total: "))

            listar_tabela(cursor, 'categorias')
            categoria_nome = validar_texto(input("Categoria: "), "Categoria")
            categoria_id = buscar_id(cursor, 'categorias', categoria_nome)

            listar_tabela(cursor, 'contas')
            conta_nome = validar_texto(input("Conta: "), "Conta")
            conta_id = buscar_id(cursor, 'contas', conta_nome)

            listar_tabela(cursor, 'naturezas')
            natureza_nome = validar_texto(input("Natureza: "), "Natureza")
            natureza_id = buscar_id(cursor, 'naturezas', natureza_nome)

            tipo_lancamento = validar_texto(input("Tipo (único, fixo, parcelado): "), "Tipo").lower()

            fixo = 1 if tipo_lancamento == 'fixo' else 0
            parcelado = 1 if tipo_lancamento == 'parcelado' else 0
            qtd_parcelas = 1

            if parcelado:
                qtd_parcelas = int(input("Quantidade de parcelas: "))
                valor_parcela = round(valor_total / qtd_parcelas, 2)
            else:
                valor_parcela = valor_total

            # Exibe resumo antes de salvar
            print("\n📝 Resumo do lançamento:")
            print(f"📅 Data: {data}")
            print(f"🧾 Descrição: {descricao}")
            print(f"💰 Valor total: R$ {valor_total:.2f}")
            print(f"💸 Valor por parcela: R$ {valor_parcela:.2f}")
            print(f"📂 Categoria: {categoria_nome}")
            print(f"🏦 Conta: {conta_nome}")
            print(f"🔎 Natureza: {natureza_nome}")
            print(f"📌 Tipo: {tipo_lancamento}")
            if parcelado:
                print(f"🔢 Parcelas: {qtd_parcelas}")

            confirmar = input("\n✅ Deseja confirmar este lançamento? (s/n): ").strip().lower()
            if confirmar != 's':
                print("❌ Lançamento cancelado pelo usuário.\n")
                continue

            # Insere o lançamento principal
            cursor.execute("""
                INSERT INTO lancamentos
                (data, descricao, valor, categoria_id, conta_id, tipo_lancamento, fixo, parcelado, qtd_parcelas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data, descricao, valor_parcela, categoria_id, conta_id,
                tipo_lancamento, fixo, parcelado, qtd_parcelas
            ))
            lancamento_id = cursor.lastrowid

            # Atualiza natureza na categoria
            cursor.execute("""
                UPDATE categorias
                SET natureza_id = %s
                WHERE id = %s
            """, (natureza_id, categoria_id))

            # Se parcelado, cria as parcelas
            if parcelado:
                for i in range(1, qtd_parcelas + 1):
                    cursor.execute("""
                        INSERT INTO parcelas (lancamento_id, numero, data, valor)
                        VALUES (%s, %s, %s, %s)
                    """, (lancamento_id, i, data, valor_parcela))

            conexao.commit()
            print("✅ Lançamento inserido com sucesso.\n")

        except Exception as e:
            print(f"❌ Erro: {e}\n")

        finally:
            conexao.close()

        repetir = input("🔁 Deseja inserir outro lançamento? (s/n): ").strip().lower()
        if repetir != 's':
            print("👋 Encerrando inserção de lançamentos.")
            break

if __name__ == '__main__':
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  #Limpa a tela
        inserir_lancamento()