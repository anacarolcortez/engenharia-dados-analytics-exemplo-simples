import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.usecases.analytics import AnalyticsService

st.set_page_config(page_title="Analytics TRF1", layout="wide")

st.title("⚖️ Processos Ambientais - TRF1")
st.markdown("---")

service = AnalyticsService()

st.subheader("Estatísticas Gerais")
stats = service.estatisticas_tempo_processo()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Média de Dias", f"{stats['media_dias']:.0f}")
col2.metric("Mediana de Dias", f"{stats['mediana_dias']:.0f}")
col3.metric("Desvio Padrão", f"{stats['desvio_padrao']:.1f}")
col4.metric("P90 (90% resolvem em)", f"{stats['p90_atraso']:.0f} dias")

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Processos por Estado")
    dados_estado = service.processos_por_estado()
    df_estado = pd.DataFrame(dados_estado)
    fig_estado = px.bar(df_estado, x='estado', y='total', 
                        color='total', labels={'total':'Nº de Processos'})
    st.plotly_chart(fig_estado, use_container_width=True)

with col_b:
    st.subheader("Tendência Mensal")
    dados_tendencia = service.processos_por_ano()
    df_tend = pd.DataFrame(dados_tendencia)
    fig_tend = px.line(df_tend, x='ano_distribuicao', y='total', markers=True)
    st.plotly_chart(fig_tend, use_container_width=True)

st.markdown("---")
st.subheader("Maiores Litigantes (Polo Passivo)")

empresas = service.empresas_mais_processadas(limit=5)
df_emp = pd.DataFrame(empresas)
fig_emp = px.bar(df_emp, x='total', y='empresa_nome', orientation='h',
                 color='total', text='total')
fig_emp.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_emp, use_container_width=True)

st.markdown("---")
st.subheader("Top 5 Litigantes por Estado")

todas_empresas = service.ranking_empresas_por_estado(limit=5)
df_geral = pd.DataFrame(todas_empresas)

estados_disponiveis = df_geral['estado'].unique()
estado_selecionado = st.selectbox("Selecione o Estado:", sorted(estados_disponiveis))

df_filtrado = df_geral[df_geral['estado'] == estado_selecionado]

if not df_filtrado.empty:
    fig_emp = px.bar(
        df_filtrado, 
        x='total', 
        y='empresa_nome', 
        orientation='h',
        color='total', 
        text='total',
        labels={'empresa_nome': 'Empresa', 'total': 'Qtd Processos'},
        color_continuous_scale='Viridis'
    )
    
    fig_emp.update_layout(
        yaxis={'categoryorder':'total ascending'},
        showlegend=False
    )
    
    st.plotly_chart(fig_emp, use_container_width=True)
    
    with st.expander("Ver detalhes em tabela"):
        st.table(df_filtrado[['ranking', 'empresa_nome', 'empresa_cnpj', 'total']])
else:
    st.info("Selecione um estado para ver o ranking.")