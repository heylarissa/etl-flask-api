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
    return dados_df.merge(tipos_df, left_on="tipo", right_on="id", how="left")


def generate_sql_insert_statements(df, output_file):
    """Gera o arquivo SQL contendo os comandos INSERT."""
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            insert_sql = f"""
            INSERT INTO dados_finais (id, nome, tipo, nome_tipo, status, created_at)
            VALUES ({row["id"]}, '{row["nome"]}', {row["tipo"]}, '{row["nome_tipo"]}', '{row["status"]}', '{row["created_at"]}');
            """
            f.write(insert_sql.strip() + "\n")


def get_aggregation_query():
    """Retorna a query para contar itens por dia e tipo."""
    return """
    SELECT DATE(created_at) AS data, nome_tipo, COUNT(*) AS total_itens
    FROM dados_finais
    GROUP BY DATE(created_at), nome_tipo
    ORDER BY data;
    """


if __name__ == "__main__":
    origem_dados_df = load_csv(ORIGEM_DADOS_CSV)
    tipos_df = load_csv(TIPOS_CSV)

    dados_criticos_df = filter_data_by_status(origem_dados_df, "CRÍTICO")
    dados_criticos_df = sort_by_created_at(dados_criticos_df)
    dados_finais_df = merge_with_types(dados_criticos_df, tipos_df)

    generate_sql_insert_statements(dados_finais_df, SQL_FILE)
    print(f"Arquivo SQL gerado: {SQL_FILE}")

    aggregation_query = get_aggregation_query()
    print("Query de agregação gerada:")
    print(aggregation_query)
