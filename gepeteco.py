import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ========== CONFIG ========== #
st.set_page_config(page_title="Dashboard RH Mágico", layout="wide")

# ========== MOCK DE DADOS ========== #
data = {
    "Employee_Name": ["Alice Johnson", "Bob Smith", "Carol White", "David Green", "Eve Black", "Frank West", "Grace Moore"],
    "Department": ["IT", "Sales", "IT", "HR", "Sales", "Finance", "Finance"],
    "Position": ["Developer", "Sales Rep", "SysAdmin", "HR Manager", "Sales Manager", "Analyst", "Controller"],
    "RaceDesc": ["White", "Black", "Asian", "White", "Hispanic", "Black", "White"],
    "Salary": [90000, 75000, 95000, 65000, 80000, 70000, 120000],
    "EngagementSurvey": [4.1, 3.8, 4.5, 3.9, 4.2, 3.0, 3.5],
    "EmploymentStatus": ["Active", "Terminated", "Active", "Active", "Active", "Active", "Active"],
    "Termd": [0, 1, 0, 0, 0, 0, 0]
}
df = pd.DataFrame(data)

# ========== SIDEBAR FILTROS ========== #
st.sidebar.header("🔍 Filtros")
departamentos = st.sidebar.multiselect("Departamento", df["Department"].unique(), default=df["Department"].unique())
cargos = st.sidebar.multiselect("Cargo", df["Position"].unique(), default=df["Position"].unique())

df_filtrado = df[(df["Department"].isin(departamentos)) & (df["Position"].isin(cargos))]

# ========== TÍTULO ========== #
st.title("🧠 Dashboard RH com Insights Estratégicos")
st.caption("Use os gráficos e insights para identificar ofensores e oportunidades.")

# ========== MÉTRICAS GERAIS ========== #
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👥 Funcionários", df_filtrado[df_filtrado["Termd"] == 0].shape[0])
with col2:
    st.metric("✅ Ativos", df_filtrado[df_filtrado["EmploymentStatus"] == "Active"].shape[0])
with col3:
    st.metric("💰 Salário Médio", f"${df_filtrado['Salary'].mean():,.0f}")

# ========== GRÁFICO SALÁRIO MÉDIO ========== #
st.subheader("💰 Salário Médio por Departamento")
sal_por_dep = df_filtrado.groupby("Department")["Salary"].mean().reset_index()

fig_sal = px.bar(sal_por_dep, x="Department", y="Salary", color="Department", template="plotly_white")
st.plotly_chart(fig_sal, use_container_width=True)

with st.expander("💡 Insight Estratégico: Salário"):
    st.markdown("Departamentos com maiores salários podem indicar talentos escassos ou políticas agressivas de retenção.")
    fig = px.box(df_filtrado, x="Department", y="Salary", color="Department", title="Distribuição Salarial", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ========== GRÁFICO ENGAJAMENTO ========== #
st.subheader("📊 Engajamento Médio por Departamento")
eng_por_dep = df_filtrado.groupby("Department")["EngagementSurvey"].mean().reset_index()

fig_eng = px.bar(eng_por_dep, x="Department", y="EngagementSurvey", color="Department", template="plotly_white")
st.plotly_chart(fig_eng, use_container_width=True)

with st.expander("💡 Insight Estratégico: Engajamento"):
    st.markdown("Departamentos com engajamento abaixo de 4 devem ser avaliados em profundidade em relação ao clima e liderança.")
    fig = px.scatter(df_filtrado, x="Salary", y="EngagementSurvey", color="Department", size="Salary", hover_name="Employee_Name", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ========== GRÁFICO DE DIVERSIDADE ========== #
st.subheader("🌎 Diversidade Étnico-Racial")
fig_div = px.pie(df_filtrado, names="RaceDesc", hole=0.4, title="Distribuição por Raça")
st.plotly_chart(fig_div, use_container_width=True)

with st.expander("💡 Insight Estratégico: Diversidade"):
    st.markdown("Monitorar diversidade garante equidade nos processos e melhora a inovação nos times.")
    race_count = df_filtrado["RaceDesc"].value_counts().reset_index()
    race_count.columns = ["Raça", "Quantidade"]
    fig = px.bar(race_count, x="Raça", y="Quantidade", color="Raça", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ========== GRÁFICO DE DESLIGAMENTOS ========== #
st.subheader("⚠️ Desligamentos por Departamento")
desligamentos = df_filtrado[df_filtrado["Termd"] == 1].groupby("Department").size().reset_index(name="Desligamentos")

if not desligamentos.empty:
    fig_desl = px.bar(desligamentos, x="Department", y="Desligamentos", color="Department", template="plotly_white")
    st.plotly_chart(fig_desl, use_container_width=True)

    with st.expander("💡 Insight Estratégico: Turnover"):
        st.markdown("Atenção aos departamentos com mais desligamentos — pode indicar problemas de clima, metas ou liderança.")
        st.dataframe(desligamentos)
else:
    st.info("Nenhum desligamento registrado no filtro atual.")

# ========== TABELA FINAL ========== #
st.markdown("---")
st.subheader("📋 Funcionários Filtrados")
st.dataframe(df_filtrado, use_container_width=True)
