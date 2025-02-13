import pandas as pd
import os

DATA_DIR = f"{os.getcwd()}/data"
ORIGEM_DADOS_CSV = os.path.join(DATA_DIR, "origem-dados.csv")
TIPOS_CSV = os.path.join(DATA_DIR, "tipos.csv")
SQL_FILE = os.path.join(DATA_DIR, "insert-dados.sql")


def load_csv(file_path):
    """Carrega um arquivo CSV em um DataFrame do pandas."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path)


def filter_data_by_status(df: pd.DataFrame, status: str):
    """Filtra os registros onde o status é 'CRÍTICO'."""
    return df[df["status"] == status]


def sort_by_created_at(df):
    """Ordena os dados pelo campo 'created_at'."""
    return df.sort_values(by="created_at")


def merge_with_types(dados_df, tipos_df):
    """Faz o merge dos dados com a tabela de tipos para incluir 'nome_tipo'."""
    print(
        dados_df.merge(tipos_df, left_on="tipo", right_on="id", how="left").rename(
            columns={"nome": "nome_tipo"}
        )
    )
    return dados_df.merge(tipos_df, left_on="tipo", right_on="id", how="left").rename(
        columns={"nome": "nome_tipo"}
    )


def generate_sql_insert_statements(df, output_file):
    """Gera o arquivo SQL contendo os comandos INSERT com tratamento de erro."""
    try:
        values = []  # Lista para armazenar os valores antes de escrever no arquivo

        for _, row in df.iterrows():
            try:
                values.append(
                    f"('{row['nome_tipo']}', {row['tipo']}, '{row['created_at']}', '{row['product_code']}', '{row['customer_code']}', '{row['status']}')"
                )
            except KeyError as e:
                print(f"Erro ao processar linha para SQL: {e}")
                continue

        if values:
            insert_sql = "INSERT INTO dados_finais (nome_tipo, tipo, created_at, product_code, customer_code, status)\nVALUES\n"
            insert_sql += ",\n".join(values) + ";"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(insert_sql)

    except Exception as e:
        print(f"Erro ao gerar arquivo SQL: {e}")


def get_aggregation_query():
    """Retorna a query para contar itens por dia e tipo."""
    return """
    SELECT DATE(created_at) AS data, nome_tipo, COUNT(*) AS total_itens
    FROM dados_finais
    GROUP BY DATE(created_at), nome_tipo
    ORDER BY data;
    """


def load_files():
    origem_dados_df = load_csv(ORIGEM_DADOS_CSV)
    tipos_df = load_csv(TIPOS_CSV)
    return origem_dados_df, tipos_df


def generate_final_data(origem_dados_df: pd.DataFrame, tipos_df: pd.DataFrame):
    dados_criticos_df = filter_data_by_status(origem_dados_df, "CRITICO")
    dados_criticos_df = sort_by_created_at(dados_criticos_df)
    dados_finais_df = merge_with_types(dados_criticos_df, tipos_df)
    return dados_finais_df


def execute_tasks():
    origem_dados_df, tipos_df = load_files()

    dados_finais_df = generate_final_data(origem_dados_df, tipos_df)
    generate_sql_insert_statements(dados_finais_df, SQL_FILE)
    print(f"Arquivo SQL gerado: {SQL_FILE}")

    aggregation_query = get_aggregation_query()
    print("Query de agregação gerada:")
    print(aggregation_query)


if __name__ == "__main__":
    execute_tasks()
