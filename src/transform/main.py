import pandas as pd
import sqlite3
from datetime import datetime
from typing import Any

def load_data(file_path: str) -> pd.DataFrame:
    """Carrega os dados de um arquivo CSV."""
    return pd.read_csv(file_path, sep=',')

def add_metadata_columns(df: pd.DataFrame, source_url: str) -> pd.DataFrame:
    """Adiciona colunas de metadados ao DataFrame."""
    df['_source'] = source_url
    df['_data_coleta'] = datetime.now()
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trata valores nulos nas colunas numéricas."""
    numeric_columns = ['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos', 'reviews_rating_number']
    for column in numeric_columns:
        df[column] = df[column].fillna(0).astype(float)
    return df

def clean_review_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Remove parênteses da coluna reviews_amount e trata valores nulos."""
    df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True).fillna(0).astype(int)
    return df

def calculate_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula os preços antigos e novos baseados nas colunas de reais e centavos."""
    df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
    df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100
    return df

def remove_old_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove as colunas antigas de preços."""
    df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)
    return df

def save_to_database(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    """Salva o DataFrame em um banco de dados SQLite."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)

def main() -> None:
    """Função principal para executar o fluxo de processamento de dados."""
    # Configurações
    file_path = '../data/data.csv'
    source_url = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
    db_path = '../data/quotes.db'
    table_name = 'mercadolivre_items'

    # Processamento dos dados
    df = load_data(file_path)
    df = add_metadata_columns(df, source_url)
    df = handle_missing_values(df)
    df = clean_review_amount(df)
    df = calculate_prices(df)
    df = remove_old_price_columns(df)

    # Salvando no banco de dados
    save_to_database(df, db_path, table_name)

if __name__ == "__main__":
    main()
