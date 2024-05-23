import streamlit as st
import pandas as pd
import sqlite3
import base64

def load_data(db_path: str, table_name: str) -> pd.DataFrame:
    """Carrega dados de uma tabela SQLite em um DataFrame do pandas."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
    return df

# Configurações da aplicação
DB_PATH = './data/quotes.db'
TABLE_NAME = 'mercadolivre_items'

# Carregar dados da tabela em um DataFrame do pandas
df = load_data(DB_PATH, TABLE_NAME)


st.set_page_config(layout='wide', page_icon=':shark:')

with st.sidebar:
    st.title('Pesquisa de Mercado - Mercado Livre')
    st.caption('Nosso objetivo é fornecer uma ferramenta que permita aos consumidores identificar as melhores ofertas de tênis esportivos no Mercado Livre, considerando fatores como preço, reputação do vendedor e avaliações dos produtos.')
    st.divider()
    url_base = st.chat_input('Insira a URL...') #https://lista.mercadolivre.com.br/tenis-corrida-masculino
    st.caption(f'URL base: {url_base if url_base is not None else "https://link-de-exemplo"}')

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.caption('GitHub')
        github_url = 'https://github.com/s2breninn/' 
        github_image_path = './assets/github.png' 
        st.markdown(
            f'<a href="{github_url}" target="_blank"><img src="{github_image_path}" width="24"></a>',
            unsafe_allow_html=True
        )

    with col2:
        st.caption('LinkedIn')
        linkedin_url = 'https://www.linkedin.com/in/breno-mendes-76820a217/'  
        linkedin_image_path = './assets/linkedin.png'
        st.markdown(
            f'<a href="{linkedin_url}" target="_blank"><img src="{linkedin_image_path}" width="24"></a>',
            unsafe_allow_html=True
        )

# Título da aplicação
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

# Melhorar o layout com colunas para KPIs
st.subheader('KPIs principais do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_items: int = df.shape[0]
col1.metric(label='Número total de itens', value=total_items)

# KPI 2: Número de marcas únicas
unique_brands: int = df['brand'].nunique()
col2.metric(label='Número de marcas únicas', value=unique_brands)

# KPI 3: Preço médio novo (em reais)
average_new_price: float = df['new_price'].mean()
col3.metric(label='Preço médio novo (R$)', value=f'{average_new_price:.2f}')

# Quais marcas são mais encontradas até a 10° página
st.subheader('Marcas mais encontradas até a 10° página')
col1, col2 = st.columns([4,2])
top10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top10_pages_brands)
col2.write(top10_pages_brands)

# KPI 4: Qual preço médio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([4,2])
df_non_zero_price = df[df['new_price'] > 0]
average_price_by_brand = df_non_zero_price.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# KPI 5: Qual a satisfação por marca
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4,2])
df_non_zero_price = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_price.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)