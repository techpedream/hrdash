import streamlit as st
import pandas as pd
import plotly.express as px

# ========== CONFIG ========== #
st.set_page_config(page_title="Dashboard RH", layout="wide")

# ========== CSS NO CÓDIGO ========== #
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    hr {
        border: 1px solid #ccc;
        margin: 20px 0;
    }
    .metric-box {
        padding: 15px;
        background-color: #ffffff;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin-left: 10px;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 260px;
        background-color: #1f2937;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        top: 130%;
        left: 50%;
        margin-left: -130px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
}

.   tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
}
    </style>
""", unsafe_allow_html=True)

# ========== CARREGAMENTO DE DADOS ========== #
df = pd.read_csv(r'C:\Users\Pedro\Documents\IAtest\archive\HRDataset_v14.csv')

st.title("📊 Dashboard de Recursos Humanos")

# ========== MÉTRICAS ========== #
col1, col2, col3 = st.columns(3)

with col1:
    total_func = df[df['Termd'] == 0].shape[0]
    st.metric("👥 Total de Funcionários", total_func)

with col2:
    ativos = len(df[df['EmploymentStatus'] == 'Active'])
    st.metric("✅ Funcionários Ativos", ativos)

with col3:
    media_sal = df['Salary'].mean()
    st.metric("Média Salarial", f"${media_sal:,.2f}")

st.markdown("---")

# ========== FILTROS ========== #
st.sidebar.header("Filtros")
departamentos = st.sidebar.multiselect(
    "Escolha os Departamentos", 
    df['Department'].unique(), 
    default=df['Department'].unique()
)

df_filtrado = df[df['Department'].isin(departamentos)]

# ========== GRÁFICO SALARIAL ========== #
st.subheader("Distribuição Salarial por Departamento")
fig_salario = px.box(
    df_filtrado,
    x="Department",
    y="Salary",
    color="Department",
    title="Distribuição de Salários",
    template="plotly_white"
)
st.plotly_chart(fig_salario, use_container_width=True)

with st.expander("💡 Insight Estratégico"):
    st.markdown("""
    <div style='background-color:#e0f3ff; padding:10px; border-radius:5px;'>
        <b>Salário de IT é maior. Sales em segundo, aparenta ter bônus de venda.</b>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico de barras de salário médio por departamento dentro do expander
    salario_departamento = df_filtrado.groupby("Department")["Salary"].mean().reset_index()
    fig_salario_departamento = px.bar(
        salario_departamento,
        x="Department",
        y="Salary",
        color="Department",
        title="Salário Médio por Departamento",
        template="plotly_white"
    )
    st.plotly_chart(fig_salario_departamento, use_container_width=True)

# ========== GÊNERO & ENGAJAMENTO ========== #
col4, col5 = st.columns(2)

with col4:
    st.subheader("Distribuição por Raça")
    fig_genero = px.pie(
        df_filtrado,
        names="RaceDesc",
        title="Proporção de Raça",
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_genero, use_container_width=True)

with col5:
    st.subheader("Engajamento por Departamento")
    engajamento = df_filtrado.groupby("Department")["EngagementSurvey"].mean().reset_index()
    fig_eng = px.bar(
        engajamento,
        x="Department",
        y="EngagementSurvey",
        color="Department",
        title="Engajamento Médio",
        template="simple_white"
    )
    st.plotly_chart(fig_eng, use_container_width=True)

# ========== TABELA FINAL ========== #
st.markdown("---")
st.subheader("Funcionários Filtrados")
st.dataframe(df_filtrado[['Employee_Name', 'Department', 'Position', 'RaceDesc', 'Salary', 'EngagementSurvey']], use_container_width=True)
