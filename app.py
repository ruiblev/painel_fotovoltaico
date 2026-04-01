import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from components.physics import compute_irradiance, compute_UI, get_characteristic_curves
from components.visuals import create_schema_svg, create_workbench_svg

# Configuração da Página
st.set_page_config(
    page_title="Simulador: Características do Painel Fotovoltaico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Global
st.markdown("""
    <style>
    .metric-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.2rem;
        font-weight: bold;
        color: #e74c3c;
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 3px solid #34495e;
        box-shadow: inset 0px 0px 10px rgba(0,0,0,0.5);
    }
    .metric-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #34495e;
        text-align: center;
        margin-bottom: 5px;
    }
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.05rem;
    }
    </style>
""", unsafe_allow_html=True)

# Estado da Sessão
if 'sim_data' not in st.session_state:
    st.session_state.sim_data = []          # sweep por distância
if 'sim_data_inc' not in st.session_state:
    st.session_state.sim_data_inc = []      # sweep por inclinação
if 'manual_data' not in st.session_state:
    st.session_state.manual_data = []

# Título
st.title("💡 Simulador: Radiação e Potência Elétrica de um Painel Fotovoltaico")
st.markdown("**Objetivo:** Investigar experimentalmente a influência da irradiância na potência elétrica fornecida por um painel fotovoltaico.")

# Menu Lateral (Modos e Configurações)
with st.sidebar:
    st.header("⚙️ Controlo da Simulação")
    
    modo = st.radio(
        "Modo de Funcionamento:",
        options=["Modo Simplificado", "Modo Avançado"],
        index=0,
        help="No Modo Simplificado o sistema executa automaticamente todo o ensaio para o fator escolhido."
    )
    
    st.divider()
    luz_ligada = st.toggle("Ligar Fonte de Radiação", value=True)
    st.subheader("Configurações Base")
    
    fonte_opcao = st.selectbox(
        "Filtro da Luz:",
        options=["Sem filtro", "Filtro Azul", "Filtro Vermelho"]
    )
    distancia = st.slider("Distância Fonte-Painel (cm):", min_value=10, max_value=100, value=30, step=5)
    inclinacao = st.slider("Inclinação do Painel (°):", min_value=0, max_value=90, value=90, step=5, help="90° perpendicular; 0° paralela.")
    
    if modo == "Modo Simplificado":
        st.divider()
        st.subheader("Ensaio Automático")
        st.info("O ensaio irá gerar automaticamente curvas para **distâncias** (15, 30, 45, 80 cm) e **inclinações** (90°, 60°, 45°, 20°, 0°), para cada fonte de luz.")
    else:
        st.divider()
        st.subheader("Variável Manipulada")
        resistencia = st.slider("Resistência do Reóstato (Ω):", min_value=1, max_value=500, value=50, step=1)
    
    st.divider()
    if st.button("🗑️ Limpar Todos os Registos"):
        st.session_state.sim_data = []
        st.session_state.sim_data_inc = []
        st.session_state.manual_data = []
        st.rerun()

# Mapeamento do Filtro
def get_filter_props(f_opcao):
    if f_opcao == "Filtro Azul":
        return 0.6, 'blue'
    elif f_opcao == "Filtro Vermelho":
        return 0.4, 'red'
    return 1.0, 'white'

filtro_fator, filtro_cor = get_filter_props(fonte_opcao)

if modo == "Modo Simplificado":
    G = compute_irradiance(distancia, inclinacao, filtro_fator)
    U, I = compute_UI(G, 50)
    fator_estudo = "Distância da Fonte"  # dummy, não é usado no simplificado novo
else:
    G = compute_irradiance(distancia, inclinacao, filtro_fator) if luz_ligada else 0.0
    U, I = compute_UI(G, resistencia)

# Construir UI Principal
tab1, tab2 = st.tabs(["🎬 Bancada de Ensaio", "📈 Tratamento de Resultados"])

with tab1:
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.markdown("### Esquema de Montagem")
        svg_bancada = create_workbench_svg(distancia, inclinacao, luz_ligada, filtro_cor, U, I)
        st.components.v1.html(svg_bancada, height=250)
        
        svg_esquema = create_schema_svg()
        st.components.v1.html(svg_esquema, height=400)

    with col2:
        st.markdown("### Gerir Ensaio")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if modo == "Modo Simplificado":
            if st.button("🚀 Iniciar Ensaio Automático", use_container_width=True, type="primary"):
                st.session_state.sim_data = []
                st.session_state.sim_data_inc = []
                
                resistencias_alvo = np.logspace(0, 3, 30)  # 1 a 1000 ohms
                fontes_para_testar = ["Sem filtro", "Filtro Azul", "Filtro Vermelho"]
                
                # --- Sweep por Distância ---
                distancias_alvo = [15, 30, 45, 80]
                for f_nome in fontes_para_testar:
                    f_fator, _ = get_filter_props(f_nome)
                    for val in distancias_alvo:
                        g_iter = compute_irradiance(val, inclinacao, f_fator)
                        for r_iter in resistencias_alvo:
                            u_iter, i_iter = compute_UI(g_iter, r_iter)
                            st.session_state.sim_data.append({
                                'Fonte de Luz': f_nome,
                                'Fator (Distância)': f"Fonte a {val} cm",
                                'Resistência (Ω)': r_iter,
                                'Tensão, U (V)': u_iter,
                                'Corrente, I (A)': i_iter,
                                'Potência, P (W)': u_iter * i_iter
                            })
                
                # --- Sweep por Inclinação ---
                inclinacoes_alvo = [90, 60, 45, 20, 0]
                for f_nome in fontes_para_testar:
                    f_fator, _ = get_filter_props(f_nome)
                    for val in inclinacoes_alvo:
                        g_iter = compute_irradiance(distancia, val, f_fator)
                        for r_iter in resistencias_alvo:
                            u_iter, i_iter = compute_UI(g_iter, r_iter)
                            st.session_state.sim_data_inc.append({
                                'Fonte de Luz': f_nome,
                                'Fator (Inclinação)': f"Painel a {val}°",
                                'Resistência (Ω)': r_iter,
                                'Tensão, U (V)': u_iter,
                                'Corrente, I (A)': i_iter,
                                'Potência, P (W)': u_iter * i_iter
                            })
                
                st.success("Ensaio concluído! Consulte os resultados na aba de Tratamento.")
                
        else:
            st.warning("**Modo Avançado:** Altere o Reóstato manualmente, registe os valores e faça os seus cálculos em baixo.")
            with st.form("modo_avancado_form"):
                input_u = st.number_input("Tensão Elétrica (V)", min_value=0.0, max_value=12.0, value=0.0, step=0.1)
                input_i = st.number_input("Corrente Elétrica (A)", min_value=0.0, max_value=5.0, value=0.0, step=0.01)
                input_p = st.number_input("Potência Elétrica (W)", min_value=0.0, max_value=20.0, value=0.0, step=0.01)
                
                sumetido = st.form_submit_button("Guardar Registo Manual")
                if sumetido:
                    st.session_state.manual_data.append({
                        'Tensão, U (V)': input_u,
                        'Corrente, I (A)': input_i,
                        'Potência, P (W)': input_p
                    })
                    st.success("Registo do aluno guardado.")


with tab2:
    color_mapping = {"Sem filtro": "#f1c40f", "Filtro Azul": "#3498db", "Filtro Vermelho": "#e74c3c"}

    def render_graphs(dataset, color_col_name, label):
        """Renderiza pares de gráficos P=f(U) e I=f(U) agrupados por valor do fator."""
        if not dataset:
            st.info(f"Ainda não existem dados para {label}. Inicie o ensaio.")
            return
        df = pd.DataFrame(dataset)
        valores_fator = df[color_col_name].unique()
        for val_fator in valores_fator:
            st.markdown(f"<h4 style='color:#2ecc71;'>📍 {val_fator}</h4>", unsafe_allow_html=True)
            df_sub = df[df[color_col_name] == val_fator]
            df_sorted  = df_sub.sort_values(by=['Fonte de Luz', 'Tensão, U (V)'])
            fig1 = px.line(df_sorted, x='Tensão, U (V)', y='Potência, P (W)',
                           color='Fonte de Luz', color_discrete_map=color_mapping, markers=True,
                           title=f"P = f(U)  |  {val_fator}")
            fig2 = px.line(df_sorted, x='Tensão, U (V)', y='Corrente, I (A)',
                           color='Fonte de Luz', color_discrete_map=color_mapping, markers=True,
                           title=f"I = f(U)  |  {val_fator}")
            for f_nome in df_sub['Fonte de Luz'].unique():
                df_val = df_sub[df_sub['Fonte de Luz'] == f_nome]
                max_idx = df_val['Potência, P (W)'].idxmax()
                max_u = df_val.loc[max_idx, 'Tensão, U (V)']
                max_i = df_val.loc[max_idx, 'Corrente, I (A)']
                max_p = df_val.loc[max_idx, 'Potência, P (W)']
                fig1.add_annotation(x=max_u, y=max_p, text="Pmax", showarrow=True, arrowhead=1, bgcolor="rgba(0,0,0,0.5)", font=dict(color="white"))
                fig2.add_annotation(x=max_u, y=max_i, text="Pmax", showarrow=True, arrowhead=1, bgcolor="rgba(0,0,0,0.5)", font=dict(color="white"))
            fig1.update_layout(hovermode="x unified")
            fig2.update_layout(hovermode="x unified")
            gcol1, gcol2 = st.columns(2)
            gcol1.plotly_chart(fig1, use_container_width=True)
            gcol2.plotly_chart(fig2, use_container_width=True)
            st.divider()

    if modo == "Modo Simplificado":
        res_tab1, res_tab2 = st.tabs(["📏 Variação de Distância", "📐 Variação de Inclinação"])
        
        with res_tab1:
            st.markdown("### Distâncias: 15, 30, 45, 80 cm — Curvas por Fonte de Luz")
            render_graphs(st.session_state.sim_data, 'Fator (Distância)', 'Distância da Fonte')
        
        with res_tab2:
            st.markdown("### Inclinações: 90°, 60°, 45°, 20°, 0° — Curvas por Fonte de Luz")
            render_graphs(st.session_state.sim_data_inc, 'Fator (Inclinação)', 'Inclinação do Painel')
    
    else:
        df = pd.DataFrame(st.session_state.manual_data)
        if df.empty:
            st.info("Ainda não existem dados registados. Registe medições na aba da Bancada de Ensaio.")
        else:
            st.dataframe(df.style.format(precision=3), use_container_width=True)
            st.markdown("### Gráficos")
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df['Tensão, U (V)'], y=df['Potência, P (W)'],
                mode='markers+lines', name='Pontos do Aluno', marker=dict(size=10, color='orange')
            ))
            fig1.update_layout(title="Potência vs Tensão Elétrica: P = f(U)", xaxis_title="U (V)", yaxis_title="P (W)")
            st.plotly_chart(fig1, use_container_width=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df['Tensão, U (V)'], y=df['Corrente, I (A)'],
                mode='markers+lines', name='Pontos do Aluno', marker=dict(size=10, color='orange')
            ))
            fig2.update_layout(title="Corrente vs Tensão Elétrica: I = f(U)", xaxis_title="U (V)", yaxis_title="I (A)")
            st.plotly_chart(fig2, use_container_width=True)
