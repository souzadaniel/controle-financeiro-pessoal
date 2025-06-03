from conexao import conectar

def excluir_lancamento():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        lanc_id = int(input("Digite o ID do lançamento que deseja excluir: "))
        cursor.execute("SELECT descricao, valor, data FROM lancamentos WHERE id = %s", (lanc_id,))
        lancamento = cursor.fetchone()

        if not lancamento:
            print("❌ Lançamento não encontrado.")
            return

        print(f"\n📌 Lançamento: {lancamento[0]} | Valor: R$ {lancamento[1]} | Data: {lancamento[2]}")
        confirmar = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Exclusão cancelada.")
            return

        cursor.execute("DELETE FROM parcelas WHERE lancamento_id = %s", (lanc_id,))
        cursor.execute("DELETE FROM lancamentos WHERE id = %s", (lanc_id,))
        conexao.commit()
        print("✅ Lançamento excluído com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        conexao.close()

if __name__ == '__main__':
    excluir_lancamento()