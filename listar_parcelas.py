from conexao import conectar

def listar_parcelas():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        lanc_id = int(input("ID do lançamento para ver parcelas: "))

        cursor.execute("SELECT * FROM lancamentos WHERE id = %s", (lanc_id,))
        if not cursor.fetchone():
            print("❌ Lançamento não encontrado.")
            return

        cursor.execute("""
            SELECT numero, data, valor, status
            FROM parcelas
            WHERE lancamento_id = %s
            ORDER BY numero
        """, (lanc_id,))
        parcelas = cursor.fetchall()

        if not parcelas:
            print("🔎 Nenhuma parcela encontrada para este lançamento.")
            return

        print(f"\n📄 Parcelas do Lançamento {lanc_id}:\n")
        for p in parcelas:
            print(f"Parcela {p[0]} - Data: {p[1]} | Valor: R${p[2]:.2f} | Status: {p[3]}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    listar_parcelas()