from conexao import conectar
from validador import (
    validar_data,
    validar_valor,
    validar_texto,
    listar_tabela,
    buscar_id
)

def editar_lancamento():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        lanc_id = int(input("\nID do lançamento a ser editado: "))
        cursor.execute("SELECT * FROM lancamentos WHERE id = %s", (lanc_id,))
        lancamento = cursor.fetchone()

        if not lancamento:
            print("❌ Lançamento não encontrado.")
            return

        # Exibe dados básicos
        print(f"\n📌 Lançamento encontrado:")
        print(f"ID: {lancamento[0]} | Valor: {lancamento[3]} | Descrição: {lancamento[2]}")
        print(f"Data: {lancamento[1]} | Categoria ID: {lancamento[4]} | Conta ID: {lancamento[5]}")
        print(f"Tipo: {lancamento[6]}")

        confirmar = input("\nEstá correto? Deseja seguir com a edição? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Edição cancelada pelo usuário.")
            return

        # Campos obrigatórios
        novo_valor = validar_valor(input("Novo valor: "))
        nova_desc = validar_texto(input("Nova descrição: "), "Descrição")
        nova_data = validar_data(input("Nova data (AAAA-MM-DD): "))

        # Categoria
        alterar_cat = input("Deseja alterar a categoria? (s/n): ").strip().lower()
        if alterar_cat == 's':
            listar_tabela(cursor, 'categorias')
            nova_categoria_nome = validar_texto(input("Nova categoria (nome exato): "), "Categoria")
            nova_categoria_id = buscar_id(cursor, 'categorias', nova_categoria_nome)
        else:
            nova_categoria_id = lancamento[4]

        # Conta
        alterar_conta = input("Deseja alterar a conta? (s/n): ").strip().lower()
        if alterar_conta == 's':
            listar_tabela(cursor, 'contas')
            nova_conta_nome = validar_texto(input("Nova conta (nome exato): "), "Conta")
            nova_conta_id = buscar_id(cursor, 'contas', nova_conta_nome)
        else:
            nova_conta_id = lancamento[5]

        # Tipo
        alterar_tipo = input("Deseja alterar o tipo (único, fixo ou parcelado)? (s/n): ").strip().lower()
        if alterar_tipo == 's':
            novo_tipo_nome = validar_texto(input("Novo tipo (único, fixo ou parcelado): "), "Tipo").lower()
        else:
            novo_tipo_nome = lancamento[6]

        # Atualização
        cursor.execute("""
            UPDATE lancamentos
            SET valor = %s,
                descricao = %s,
                data = %s,
                categoria_id = %s,
                conta_id = %s,
                tipo_lancamento = %s
            WHERE id = %s
        """, (
            novo_valor,
            nova_desc,
            nova_data,
            nova_categoria_id,
            nova_conta_id,
            novo_tipo_nome,
            lanc_id
        ))

        conexao.commit()
        print("\n✅ Lançamento atualizado com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        conexao.close()

if __name__ == '__main__':
    editar_lancamento()