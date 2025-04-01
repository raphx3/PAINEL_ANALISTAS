#%% MODULOS
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import altair as alt

#%% DADOS
tempo = pd.date_range(start='2025/01/01',end='2025/12/31', freq='D')
temperatura = np.random.normal (25,10, len (tempo))
umidade = np.random.normal (70,10, len(tempo))
precipitacao = np.random.normal (500,50, len(tempo))


dados = pd.DataFrame ({'tempo':tempo,'temperatura':temperatura,'umidade':umidade, 'precipitacao':precipitacao}).set_index ('tempo')
dados ['10D_mean_temperatura'] = dados ['temperatura'].rolling(10).mean().bfill()
dados ['10D_mean_umidade'] = dados ['umidade'].rolling(10).mean().bfill()
dados ['10D_mean_precipitacao'] = dados ['precipitacao'].rolling(10).mean().bfill()

#%% ESTRUTURA STREAMLIT

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
#st.logo (r'C:/Users/Rafael Alvarenga UMI/Desktop/PD_METEO/REPORTES/DASHBOARD/LOGO_UMISAN.png')
st.title ('Reporte operacional para controle interno')
#st.sidebar.title("Configurações")


#%% TEXTO 1
st.subheader ('Sobre')
st.markdown('Painel para a análise e tomada de decisões a partir de dados <b style="color:black">meteoceanográficos</b> referentes ao projeto. ', unsafe_allow_html=True)
st.markdown('A versão atual conta com dados fictícios de temperatura, umidade e precipitação sendo resumidas como estando <b style="color:green">aprovadas</b> ou <b style="color:red">reprovadas</b> considerando os critérios técnicos descritos em "Metologia".', unsafe_allow_html=True)


#%% TEXTO 2

st.subheader ('Resumo')

media_temperatura =dados['temperatura'].mean().round(2)
maxima_temperatura =dados['temperatura'].max().round(2)
minima_temperatura =dados['temperatura'].min().round(2)

media_umidade=dados['umidade'].mean().round(2)
maxima_umidade=dados['umidade'].max().round(2)
minima_umidade=dados['umidade'].min().round(2)

media_precipitacao=dados['precipitacao'].mean().round(2)
maxima_precipitacao=dados['precipitacao'].max().round(2)
minima_precipitacao=dados['precipitacao'].min().round(2)

st.markdown(f'A temperatura apresentou valores médio de {media_temperatura}, máxima de {maxima_temperatura} e mínima de {minima_temperatura}; A umidade apresentou valores médio de {media_umidade}, máxima de {maxima_umidade} e mínima de {minima_umidade}; A precipitacao apresentou valores médio de {media_precipitacao}, máxima de {maxima_precipitacao} e mínima de {minima_precipitacao}', unsafe_allow_html=True)
st.markdown('Os valores encontrados estão <b style="color:green">aprovadas</b> considerando os limites operacionais e ambientais esperados e os filtros lógicos baseados na padronização QUARTOD.', unsafe_allow_html=True)


#%% CARDS DE RESUMO


col1, col2, col3 = st.columns (3)


media_temperatura =dados['temperatura'].mean().round(2) 
atual_temperatura = dados['temperatura'].iloc[-1].round(2)
delta_temperatura = (atual_temperatura - media_temperatura).round (2)
col1.metric (label='Temperatura', value=f'{atual_temperatura}°C', border=True, delta=f'{media_temperatura}°C')


media_umidade=dados['umidade'].mean().round(2) 
atual_umidade = dados['umidade'].iloc[-1].round(2)
delta_umidade = (atual_umidade - media_umidade).round (2)
col2.metric (label='Umidade', value=f'{atual_umidade}%', border=True, delta=f'{delta_umidade}%')

media_precipitacao=dados['precipitacao'].mean().round(2) 
atual_precipitacao = dados['precipitacao'].iloc[-1].round(2)
delta_precipitacao = (atual_precipitacao - media_precipitacao).round (2)
col3.metric (label='Precipitacao', value=f'{atual_precipitacao}mm', border=True, delta=f'{delta_precipitacao}mm')

#%% TEXTO 2

st.subheader ('Série temporal')
st.markdown('O conjunto de dados é composto por dados desde 01/01/2025 até 31/12/2025 estando disponíveis para análise para as 3 variáveis.', unsafe_allow_html=True)


#%% PLOTS PLOTLY


# SERIE TEMPORAL


# Dados de exemplo
tempo = pd.date_range(start='2025/01/01', end='2025/12/31', freq='D')
temperatura = np.random.normal(25, 10, len(tempo))
umidade = np.random.normal(70, 10, len(tempo))
precipitacao = np.random.normal(500, 50, len(tempo))

# Criando o DataFrame
dados = pd.DataFrame({
    'tempo': tempo,
    'temperatura': temperatura,
    'umidade': umidade,
    'precipitacao': precipitacao
}).set_index('tempo')

# Calculando as médias móveis
dados['10D_mean_temperatura'] = dados['temperatura'].rolling(10).mean().bfill()
dados['10D_mean_umidade'] = dados['umidade'].rolling(10).mean().bfill()
dados['10D_mean_precipitacao'] = dados['precipitacao'].rolling(10).mean().bfill()

# Seletor de variável para visualização
variavel = st.selectbox(
    'Escolha a variável a ser exibida:',
    ['Temperatura', 'Umidade', 'Precipitação']
)

# Seletor de intervalo de tempo
data_inicio = st.date_input('Data de Início', dados.index.min())
data_fim = st.date_input('Data de Fim', dados.index.max())

# Filtrando os dados pelo intervalo de tempo selecionado
dados_filtrados = dados[(dados.index >= pd.to_datetime(data_inicio)) & (dados.index <= pd.to_datetime(data_fim))]

# Mapeando a variável escolhida para as colunas correspondentes
if variavel == 'Temperatura':
    y_data = dados_filtrados['temperatura']
    y_rolling = dados_filtrados['10D_mean_temperatura']
    yaxis_title = 'Temperatura (°C)'
    tabela = dados_filtrados[['temperatura', '10D_mean_temperatura']].reset_index()
elif variavel == 'Umidade':
    y_data = dados_filtrados['umidade']
    y_rolling = dados_filtrados['10D_mean_umidade']
    yaxis_title = 'Umidade (%)'
    tabela = dados_filtrados[['umidade', '10D_mean_umidade']].reset_index()
else:  # Precipitação
    y_data = dados_filtrados['precipitacao']
    y_rolling = dados_filtrados['10D_mean_precipitacao']
    yaxis_title = 'Precipitação (mm)'
    tabela = dados_filtrados[['precipitacao', '10D_mean_precipitacao']].reset_index()

# Renomeando as colunas para corresponder à variável escolhida
tabela.columns = ['Tempo', variavel, 'Média Móvel - 10 dias']

# Criando o gráfico
fig = go.Figure()

# Adicionando as linhas do gráfico com as cores fixas
fig.add_trace(go.Scatter(
    x=dados_filtrados.index,
    y=y_data,
    mode='lines',
    name=f'{variavel} observada',
    line=dict(color='gray'),  # Cor fixa para o gráfico observado
    opacity=0.3
))

fig.add_trace(go.Scatter(
    x=dados_filtrados.index,
    y=y_rolling,
    mode='lines',
    name='Média móvel - 10 dias',
    line=dict(color='black')  # Cor fixa para a média móvel
))

# Atualizando o layout do gráfico
fig.update_layout(
    title=f'Série temporal de {variavel}',
    xaxis_title='Tempo',
    yaxis_title=yaxis_title,
    template='ggplot2',
    legend_title='',
    plot_bgcolor='white',
    legend=dict(
        x=0.01,  # Posição horizontal da legenda (0 é esquerda, 1 é direita)
        y=0.99,  # Posição vertical da legenda (0 é inferior, 1 é superior)
        xanchor='left',  # Ancoragem da legenda no eixo X (esquerda, centro, direita)
        yanchor='top',  # Ancoragem da legenda no eixo Y (inferior, centro, superior)
        orientation='h'  # Orientação horizontal ('h') ou vertical ('v')
    )
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)

# Exibindo a tabela com a variável escolhida, média móvel e tempo
# A tabela agora vai ocupar toda a largura disponível
st.dataframe(tabela.round(2), use_container_width=True)

#%% TEXTO 4
st.subheader ('Matriz de qualidade')
st.markdown('A matriz resume o resultado dos diversos parâmetros considerados durante a etapa de processamento e filtragem dos dado brutos. Valores acima de 10% são considerados críticos e devem ser reportados e investigados.', unsafe_allow_html=True)

#%% MAPA DE CALOR PLOTLY

# # Carregar a matriz do arquivo Excel
# matriz = pd.read_excel(r'C:/Users/Rafael Alvarenga UMI/Desktop/PD_METEO/REPORTES/DASHBOARD/RESULTADOS_MATRIZ_COM_ERROS.xlsx')

# # Definindo a coluna 'Parametro' como índice
# matriz = matriz.set_index('Parametro').transpose()

# # Convertendo a matriz em formato 'long' para usar no Altair
# matriz_long = matriz.reset_index().melt(id_vars=['index'], var_name='Testes', value_name='% de Erros')

# # Criando o heatmap com Altair
# heatmap = alt.Chart(matriz_long).mark_rect().encode(
#     x='Testes:N',
#     y='index:N',
#     color='% de Erros:Q',
#     tooltip=['Testes', 'index', '% de Erros']
# ).properties(
#     width='container',  # Ajusta a largura ao tamanho do container do Streamlit
#     height=400  # Ajuste a altura conforme necessário
# ).configure_view(
#     strokeWidth=0  # Remove as bordas
# )

# # Exibindo o gráfico no Streamlit
# st.altair_chart(heatmap, use_container_width=True)







import pandas as pd
import streamlit as st
import altair as alt

# Dados fornecidos (com tamanho consistente)
dados = {
    'Parametro': [
        'detectar_platos', 'gradiente_de_amplitude_do_sinal', 'identificar_dados_nulos',
        'identificar_duplicatas_tempo', 'identificar_gaps', 'lt_time_series_rate_of_change',
        'max_min_test', 'range_check_environment', 'range_check_sensors', 'spike_test',
        'st_time_series_segment_shift', 'taxa_de_mudanca_vertical', 'teste_continuidade_tempo',
        'time_offset', 'verifica_dados_repetidos', 'verificar_altura_max_vs_sig',
        'verificar_temperatura_vs_ponto_de_orvalho', 'verificar_velocidade_vs_rajada'
    ],
    'Amplitude_Cell#1': [0.0]*18,
    'Speed(m/s)_Cell#1': [0.0, 0.0, 0.0, 0.0, 18.77, 0.0, 0.0, 33.58, 0.0, 0.0, 0.0, 0.0, 81.77, 76.78, 0.0, 0.0, 0.0, 0.0],
    'Direction_Cell#1': [0.0]*18,
    'Direction_Cell#2': [0.0]*18,
    'Amplitude_Cell#2': [27.76, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 94.58, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Speed(m/s)_Cell#2': [0.0]*18,
    'Amplitude_Cell#3': [0.0, 0.0, 62.91, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Speed(m/s)_Cell#3': [0.0]*18,
    'Direction_Cell#3': [0.0, 0.0, 0.0, 0.0, 96.43, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Direction_Cell#4': [0.0]*18,
    'Amplitude_Cell#4': [0.0]*18,
    'Speed(m/s)_Cell#4': [0.0]*18,
    'Amplitude_Cell#5': [0.0]*18,
    'Speed(m/s)_Cell#5': [0.0]*18,
    'Direction_Cell#5': [0.0]*18,
    'Amplitude_Cell#6': [0.0]*18,
    'Speed(m/s)_Cell#6': [0.0]*18,
    'Direction_Cell#6': [0.0]*18,
    'Amplitude_Cell#7': [0.0]*18,
    'Speed(m/s)_Cell#7': [0.0]*18,
}

# Convertendo para um DataFrame
matriz = pd.DataFrame(dados)

# Garantindo que 'Parametro' tenha 18 elementos
dados['Parametro'] = dados['Parametro'][:18]

# Convertendo para DataFrame novamente
matriz = pd.DataFrame(dados)

# Definindo 'Parametro' como índice
matriz = matriz.set_index('Parametro').transpose()

# Convertendo para formato 'long'
matriz_long = matriz.reset_index().melt(id_vars=['index'], var_name='Testes', value_name='% de Erros')

# Criando o heatmap com Altair
heatmap = alt.Chart(matriz_long).mark_rect().encode(
    x='Testes:N',
    y='index',
    color='% de Erros:Q',
    tooltip=['Testes', 'index', '% de Erros']
).properties(
    width='container',  # Ajusta a largura ao tamanho do container do Streamlit
    height=600  # Ajuste a altura para maximizar o gráfico
).configure_axis(
    labelFontSize=0,  # Remove as labels dos eixos
    titleFontSize=14   # Mantém o título dos eixos com tamanho 14
).configure_view(
    strokeWidth=0  # Remove as bordas
)

# Exibindo o gráfico no Streamlit
st.altair_chart(heatmap, use_container_width=True)







#%% MAPA DE CALOR PLOTLY

#st.markdown('É possível interagir com a tabela abaixo mas recomenda-se que se faça o dowload e uma investigação mais detalhada dos resultados apresentados.', unsafe_allow_html=True)



# Carregar a matriz do arquivo Excel
#matriz = pd.read_excel(r'C:/Users/Rafael Alvarenga UMI/Desktop/PD_METEO/REPORTES/DASHBOARD/RESULTADOS_MATRIZ_COM_ERROS.xlsx')

# Definindo a coluna 'Parametro' como índice
#matriz = matriz.set_index('Parametro')

# Estilizando a tabela com arredondamento apenas para exibição, sem alterar o DataFrame original
#st.dataframe(matriz.round(2))


#%% TESTE










