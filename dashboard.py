import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

st.set_page_config(page_title='Previsão de Vendas - Rossmann', layout='wide')


@st.cache_data
def carregar_dados():
    df = pd.read_csv('previsoes_teste.csv', parse_dates=['Date'])
    return df

dados = carregar_dados()

st.title('📈 Previsão de Vendas - Rossmann Store Sales')
st.markdown('Comparação entre vendas reais e previstas pelo modelo LightGBM')


lojas_disponiveis = sorted(dados['Store'].unique())
loja_selecionada = st.sidebar.selectbox('Selecione a loja', lojas_disponiveis)

dados_loja = dados[dados['Store'] == loja_selecionada]


mae = mean_absolute_error(dados_loja['Sales'], dados_loja['Previsao'])
rmse = np.sqrt(mean_squared_error(dados_loja['Sales'], dados_loja['Previsao']))
mape = np.mean(np.abs((dados_loja['Sales'] - dados_loja['Previsao']) / dados_loja['Sales'])) * 100

col1, col2, col3 = st.columns(3)
col1.metric('MAE', f'{mae:.2f}')
col2.metric('RMSE', f'{rmse:.2f}')
col3.metric('MAPE', f'{mape:.2f}%')


fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(dados_loja['Date'], dados_loja['Sales'], label='Real', marker='o')
ax.plot(dados_loja['Date'], dados_loja['Previsao'], label='Previsto', marker='x')
ax.set_title(f'Previsão vs. Real - Loja {loja_selecionada}')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)
st.markdown('---')
st.subheader('📊 Comparação de Modelos (Loja 1)')

col1, col2 = st.columns(2)
with col1:
    st.markdown('**LightGBM**')
    st.metric('MAE', '315.44')
    st.metric('RMSE', '418.61')
    st.metric('MAPE', '7.02%')
with col2:
    st.markdown('**SARIMA**')
    st.metric('MAE', '641.82')
    st.metric('RMSE', '726.30')
    st.metric('MAPE', '15.25%')

st.caption('O LightGBM superou o SARIMA por conseguir incorporar variáveis externas (promoções, feriados) e aprender padrões entre múltiplas lojas simultaneamente, enquanto o SARIMA modela apenas a série histórica isolada de uma única loja.')