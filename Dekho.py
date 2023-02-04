import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import locale
import plotly.express as px
from currency_converter import CurrencyConverter

c = CurrencyConverter()

# Configuração da pagina de streamlit
icone = Image.open('./assets/icone_url.png')
st.set_page_config(page_title="Sobre DEKHO", layout="wide", page_icon=icone)

df = pd.read_csv('./dataset/CAR DETAILS FROM CAR DEKHO.csv')
# Criação de coluna de modelo > primeira palavra da coluna "name"
df["marca"] = df.name.apply(lambda x : ' '.join(x.split(' ')[:1]))
df['marca'].value_counts()

# Criação dos container da pagina Dekho
cabecalho = st.container()
dadosGerais = st.container()
graficos = st.container()


with cabecalho:
    back_img = Image.open('assets/logo.jpeg')
    st.title("Informações gerais sobre Dekho")
    st.image(back_img)
    st.subheader("Quem é Dekho")
    
    st.markdown("""CarDekho é a principal plataforma de pesquisa e compra de carros seminovos da Índia.""")
    
    st.markdown("""O seu diferencial é a sua experiência com usuário por sempre entregar as informações detalhadas, também tem disponível avaliações de especialistas, é possível realizar comparações, bem como vídeos e fotos de todas as marcas e modelos de carros disponíveis na Índia. A empresa tem parcerias com muitos fabricantes de automóveis, mais de 4.000 revendedores de automóveis e várias instituições financeiras para facilitar a compra de veículos""")

with dadosGerais:
    # --------------------------- CABEÇALHO---------------------
    st.subheader("Dados anuais sobre a Dekho")

    anos = pd.Series(df['year'].unique()).sort_values(ascending=False)
    # ------------------------ SELECIONAR ANO ---------------------------      
    ano_selecionado = st.selectbox(label=
    'Selecione uma ano',
    options=anos,
    index=0
    )
    
    # FILTRO DE ANO    
    df_ano = df[df['year'] == ano_selecionado]
    
    # ------------------------ CARD 1 & 2 ---------------------------      
    faturamento_numb = df_ano['selling_price'].sum()
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    faturamento = locale.currency(c.convert(faturamento_numb, 'USD', 'BRL'), grouping=True)
    
    qtdVendas = df_ano['selling_price'].count() 
    qtd_marcas = len(df_ano.groupby(['marca']))
    
    
    fat, qtdVeic = st.columns(2)
    fat.metric("Faturamento",faturamento)
    qtdVeic.metric("Quantidade vendidas", qtdVendas)
    
    # ------------------------ CARD 3 & 4---------------------------
    precoMedio = faturamento_numb / qtdVendas
    precoMedioValor = locale.currency(c.convert(precoMedio, 'USD', 'BRL'), grouping=True)    
    precoMedio, qtdMarca = st.columns(2)
    
    precoMedio.metric("Preço medio", precoMedioValor)
    qtdMarca.metric("Mix de marcas", qtd_marcas)

with graficos:
    # GRAFICO 1
    st.subheader("Média do preço de venda por marca")
    fig1 = px.histogram(df_ano, x="marca", y="selling_price",
            histfunc='avg',
            height=400, 
            labels={'marca': 'Marca do carro', 'selling_price': 'Preço de venda'})
    fig1.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig1)
     
    # GRAFICO 2
    st.subheader("Preço de vendas VS Número de proprietários e Transmissão")
    fig2 = px.box(df_ano, x="owner", y="selling_price", color="transmission", 
            labels={'Owner': 'Número de proprietários', 'selling_price': 'Preço de venda'}
            )
    st.plotly_chart(fig2)
    
    # GRAFICO 3
    st.subheader("Preço de vendas VS Tipo de combustivel")
    fig3 = px.box(df_ano, x="fuel", y="selling_price", 
              labels={'fuel': 'Tipo de combustivel', 'selling_price': 'Preço de venda'},            
              hover_data=['name', 'year', 'selling_price', 'km_driven'] 
             )
    st.plotly_chart(fig3)
