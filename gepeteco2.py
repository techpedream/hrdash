import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Ninebox + Avaliação de Competências com Insights", layout="wide")

# CSS custom para cartão da ficha + styling expanders e texto
st.markdown("""
<style>
/* Cartão bonito para ficha */
.ficha-cartao {
    background: #f9fafb;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 10px rgb(0 0 0 / 0.1);
    margin-bottom: 1rem;
}

/* Título e insight juntos dentro do expander */
.expander-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Texto do insight ao lado do título dentro do expander */
.insight-text {
    font-size: 0.9rem;
    font-style: italic;
    color: #666;
    max-width: 300px;
    margin-left: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Dados Exemplo
df = pd.DataFrame({
    "Nome": ["Alice", "Bruno", "Carla", "Daniel", "Eduardo", "Fernanda", "Gustavo", "Helena"],
    "Performance": [7, 9, 4, 6, 8, 5, 3, 7],
    "Potencial": [6, 8, 5, 4, 9, 3, 7, 6],
    "Competencia_1": [3, 4, 2, 5, 4, 3, 4, 5],
    "Competencia_2": [4, 5, 3, 3, 5, 4, 2, 4],
    "Competencia_3": [5, 4, 2, 4, 5, 3, 3, 5],
    "Competencia_4": [3, 5, 4, 2, 4, 5, 3, 4],
    "Competencia_5": [4, 3, 5, 4, 3, 4, 5, 3],
})

# ====== FILTRO ======
st.sidebar.header("Filtro")
nome_filtro = st.sidebar.multiselect("Selecione colaboradores", options=df["Nome"].tolist(), default=df["Nome"].tolist())

df_filtrado = df[df["Nome"].isin(nome_filtro)]

# ====== FUNÇÕES DE GRÁFICOS ======

def ninebox_chart(df):
    fig = px.scatter(
        df,
        x="Potencial",
        y="Performance",
        hover_name="Nome",
        labels={"Potencial": "Potencial", "Performance": "Performance"},
        title="Ninebox: Potencial x Performance",
        width=500,
        height=450,
    )
    fig.update_traces(marker=dict(size=16, color='royalblue'), selector=dict(mode='markers'))
    fig.update_layout(
        xaxis=dict(range=[0,10], dtick=1),
        yaxis=dict(range=[0,10], dtick=1),
        hovermode="closest",
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig

def radar_competencias(df, nome):
    pessoa = df[df["Nome"] == nome].iloc[0]
    categorias = ["Competencia_1", "Competencia_2", "Competencia_3", "Competencia_4", "Competencia_5"]
    valores = [pessoa[c] for c in categorias]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores + [valores[0]],
        theta=categorias + [categorias[0]],
        fill='toself',
        name=nome,
        marker_color='crimson'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,5],
                dtick=1
            )),
        showlegend=False,
        title=f"Avaliação de Competências - {nome}",
        width=500,
        height=450,
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig

# ====== LAYOUT PRINCIPAL ======
st.title("🎯 Ninebox e Avaliação de Competências")

col1, col2, col3 = st.columns([1.1,1,1])

# -- COLUNA 1: FILTRO + NINEBOX + FICHA ESTILIZADA --
with col1:
    st.header("Ninebox")
    fig_ninebox = ninebox_chart(df_filtrado)
    st.plotly_chart(fig_ninebox, use_container_width=True)
    
    nome_selecionado = st.selectbox("Selecione colaborador para ficha e radar:", df_filtrado["Nome"].tolist())
    
    pessoa = df_filtrado[df_filtrado["Nome"] == nome_selecionado].iloc[0]
    ficha_md = f"""
    <div class="ficha-cartao">
        <h3>Ficha do Colaborador</h3>
        <p><strong>Nome:</strong> {pessoa['Nome']}</p>
        <p><strong>Performance:</strong> {pessoa['Performance']}</p>
        <p><strong>Potencial:</strong> {pessoa['Potencial']}</p>
    </div>
    """
    st.markdown(ficha_md, unsafe_allow_html=True)

# -- COLUNA 2: RADAR + TITULO COM INSIGHT AO LADO --
with col2:
    st.markdown(
        """
        <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom:0.5rem;">
            <h3 style="margin:0;">Avaliação de Competências</h3>
            <div style="font-size:0.9rem; font-style:italic; color:#555; max-width:300px; padding-left:1rem;">
                Competências alinhadas com a estratégia. Observe os pontos fortes e oportunidades.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    fig_radar = radar_competencias(df_filtrado, nome_selecionado)
    st.plotly_chart(fig_radar, use_container_width=True)

# -- COLUNA 3: INSIGHTS EXPANDIVEIS COM SETINHA E TEXTO AO LADO --
with col3:
    with st.expander("📊 Distribuição de Performance"):
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">Insight</h4>
                <div style="font-size:0.9rem; font-style:italic; color:#666; max-width:280px; margin-left:1rem;">
                    A maioria está com performance entre 5 e 8, indicando boa entrega, mas atenção aos que estão abaixo de 5.
                </div>
            </div>
            """, unsafe_allow_html=True)
        fig1 = px.histogram(df_filtrado, x="Performance", nbins=8, labels={"Performance":"Performance"}, width=400, height=180)
        st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📊 Distribuição de Potencial"):
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">Insight</h4>
                <div style="font-size:0.9rem; font-style:italic; color:#666; max-width:280px; margin-left:1rem;">
                    Potenciais altos (>7) são poucos, foco no desenvolvimento deles para sucessão.
                </div>
            </div>
            """, unsafe_allow_html=True)
        fig2 = px.histogram(df_filtrado, x="Potencial", nbins=8, labels={"Potencial":"Potencial"}, width=400, height=180)
        st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("🚩 Ofensores: Baixa Performance"):
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">Alerta</h4>
                <div style="font-size:0.9rem; font-style:italic; color:#666; max-width:280px; margin-left:1rem;">
                    Colaboradores abaixo de 5 precisam de atenção e planos de ação.
                </div>
            </div>
            """, unsafe_allow_html=True)
        baixa_perf = df_filtrado[df_filtrado["Performance"] < 5]
        st.dataframe(baixa_perf[["Nome", "Performance", "Potencial"]], height=140)

    with st.expander("🚩 Ofensores: Baixo Potencial"):
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">Alerta</h4>
                <div style="font-size:0.9rem; font-style:italic; color:#666; max-width:280px; margin-left:1rem;">
                    Potencial abaixo de 5 indica necessidade de reavaliação de carreira.
                </div>
            </div>
            """, unsafe_allow_html=True)
        baixa_pot = df_filtrado[df_filtrado["Potencial"] < 5]
        st.dataframe(baixa_pot[["Nome", "Performance", "Potencial"]], height=140)
