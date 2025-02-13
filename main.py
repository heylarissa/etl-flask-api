from src.utils.read_csv_data import (
    load_files,
    generate_final_data,
    generate_sql_insert_statements,
    SQL_FILE,
    get_aggregation_query,
)
from src.utils.unzip_files import unzip_files

if __name__ == "__main__":
    unzip_files()
    origem_dados_df, tipos_df = load_files()

    dados_finais_df = generate_final_data(origem_dados_df, tipos_df)
    generate_sql_insert_statements(dados_finais_df, SQL_FILE)
    print(f"Arquivo SQL gerado: {SQL_FILE}")

    aggregation_query = get_aggregation_query()
    print("Query de agregação gerada:")
    print(aggregation_query)
