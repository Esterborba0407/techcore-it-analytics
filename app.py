"""TechCore IT Analytics — dashboard interativo de Governança e Gestão de TI.

Ponto de entrada da aplicação Streamlit. A lógica de dados, insights e
geração de relatórios fica isolada em `src/`, mantendo este arquivo focado
em layout e interação.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import (
    MESES_ORDEM,
    filter_areas,
    filter_projects,
    filter_regions,
    filter_tickets,
    filter_monthly,
    load_all,
)
from src.insights import (
    fmt_moeda,
    fmt_pct,
    insights_contratos,
    insights_financeiros,
    insights_fornecedores,
    insights_projetos,
    insights_service_desk,
    resumo_financeiro,
)
from src.report import montar_relatorio_markdown, montar_relatorio_pdf
from src.styles import CSS

st.set_page_config(
    page_title="TechCore IT Analytics",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)

dados = load_all()

# ============================================================ Sidebar =====
with st.sidebar:
    st.markdown("## 🔷 TechCore")
    st.caption("Solutions")
    st.markdown("---")
    st.markdown("#### 🎛️ Filtros")

    mes_ini, mes_fim = st.select_slider(
        "Período",
        options=MESES_ORDEM,
        value=(MESES_ORDEM[0], MESES_ORDEM[-1]),
    )
    regioes_sel = st.multiselect(
        "Região",
        options=list(dados["regions"]["regiao"]),
        help="Deixe vazio para considerar todas as regiões.",
    )
    areas_sel = st.multiselect(
        "Área de TI",
        options=list(dados["areas"]["area"]),
        help="Deixe vazio para considerar todas as áreas.",
    )

    st.markdown("---")
    pagina = st.radio(
        "Navegação",
        [
            "Visão Geral",
            "Financeiro",
            "Projetos",
            "Fornecedores",
            "Contratos",
            "Service Desk",
            "🧠 Gerador de Relatórios",
        ],
    )
    st.markdown("---")
    st.caption("TechCore IT Analytics")
    st.caption("Governança de TI • Gestão de Custos • Projetos • SLA")
    st.markdown(
        "<div class='footer-note'>Desenvolvido por Ester Santos da Cruz Borba</div>",
        unsafe_allow_html=True,
    )

# ==================================================== Dados filtrados =====
monthly_f = filter_monthly(dados["monthly"], mes_ini, mes_fim)
tickets_f = filter_tickets(dados["tickets"], mes_ini, mes_fim)
areas_f = filter_areas(dados["areas"], areas_sel)
regions_f = filter_regions(dados["regions"], regioes_sel)
projects_f = filter_projects(dados["projects"], areas_sel, [])

# ============================================================== Hero ======
st.markdown('<div class="badge-live"><span class="dot"></span> Dados atualizados</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Dashboard de Gestão de TI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Indicadores financeiros e operacionais para uma tomada de decisão mais estratégica.</div>',
    unsafe_allow_html=True,
)
st.markdown("###")


def gauge_consumo(consumo_pct: float, titulo: str = "% do orçamento consumido") -> go.Figure:
    """Cria um velocímetro (gauge) plotly para o consumo orçamentário ou SLA."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(consumo_pct * 100, 1),
            number={"suffix": "%", "font": {"color": "#ffffff"}},
            title={"text": titulo, "font": {"size": 13, "color": "#9eacd0"}},
            gauge={
                "axis": {"range": [0, 130], "tickcolor": "#5a6a9e"},
                "bar": {"color": "#7c8bff"},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 80], "color": "#123024"},
                    {"range": [80, 100], "color": "#332a10"},
                    {"range": [100, 130], "color": "#3a1420"},
                ],
                "threshold": {"line": {"color": "#ff4f81", "width": 3}, "thickness": 0.85, "value": 100},
            },
        )
    )
    fig.update_layout(
        height=230,
        margin=dict(l=25, r=25, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f5f7ff"},
    )
    return fig


def render_alertas(projects_df: pd.DataFrame, tickets_df: pd.DataFrame) -> None:
    """Renderiza cartões de alerta gerados dinamicamente a partir dos dados filtrados."""
    estourados = projects_df[projects_df["consumo_pct"] > 1]
    if not estourados.empty:
        nomes = ", ".join(estourados["projeto"].tolist())
        st.markdown(
            f'<div class="alert alert-danger">🔴 <b>{len(estourados)} projeto(s) acima do orçamento</b><br>{nomes}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="alert alert-success">🟢 <b>Projetos sob controle</b><br>Nenhum projeto ultrapassou o orçamento.</div>',
            unsafe_allow_html=True,
        )

    proximos = dados["contracts"][dados["contracts"]["dias_para_vencer"] <= 60]
    if not proximos.empty:
        st.markdown(
            f'<div class="alert alert-warning">🟡 <b>{len(proximos)} contrato(s)</b><br>Próximos do vencimento (≤ 60 dias).</div>',
            unsafe_allow_html=True,
        )

    top_fornecedor = dados["suppliers"].sort_values("valor", ascending=False).iloc[0]
    participacao = top_fornecedor["valor"] / dados["suppliers"]["valor"].sum()
    if participacao > 0.3:
        st.markdown(
            f'<div class="alert alert-warning">🟠 <b>{top_fornecedor["fornecedor"]}</b><br>'
            f"Concentra {fmt_pct(participacao)} do gasto com fornecedores.</div>",
            unsafe_allow_html=True,
        )

    sla_medio = tickets_df["sla_pct"].mean() if not tickets_df.empty else 0
    if sla_medio >= 90:
        st.markdown(
            f'<div class="alert alert-success">🟢 <b>SLA</b><br>{sla_medio:.0f}% dos chamados dentro do SLA.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="alert alert-warning">🟡 <b>SLA abaixo da meta</b><br>Média de {sla_medio:.0f}% no período.</div>',
            unsafe_allow_html=True,
        )


# ========================================================= Visão Geral ====
if pagina == "Visão Geral":
    r = resumo_financeiro(monthly_f)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Orçamento de TI", fmt_moeda(r["orcamento"]))
    k2.metric("Realizado", fmt_moeda(r["realizado"]))
    k3.metric("Saldo disponível", fmt_moeda(r["saldo"]))
    k4.metric("Previsão de fechamento", fmt_moeda(r["previsao_fechamento"]))
    k5.metric("% orçamento consumido", fmt_pct(r["consumo"]))

    st.markdown("###")
    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        st.subheader("Orçamento x Realizado")
        fig = px.bar(
            monthly_f, x="mes", y=["orcamento", "realizado"],
            barmode="group",
            labels={"value": "Valor (R$)", "variable": "", "mes": ""},
            color_discrete_sequence=["#3a4f9e", "#7c8bff"],
        )
        fig.update_layout(
            template="plotly_dark", height=320, margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", y=1.12), paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Custos por Área")
        fig = px.pie(areas_f, names="area", values="valor", hole=0.62)
        fig.update_layout(
            template="plotly_dark", height=250, margin=dict(l=5, r=5, t=10, b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True, legend=dict(font=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(gauge_consumo(r["consumo"]), use_container_width=True)

    with col3:
        st.subheader("Custos por Fornecedor")
        fig = px.bar(dados["suppliers"].sort_values("valor"), x="valor", y="fornecedor", orientation="h")
        fig.update_layout(
            template="plotly_dark", height=350, margin=dict(l=5, r=5, t=20, b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.7, 1, 1])

    with col1:
        st.subheader("Projetos de TI")
        disp = projects_f.copy()
        disp["consumo_pct_disp"] = disp["consumo_pct"] * 100
        st.dataframe(
            disp[["projeto", "area", "orcamento", "realizado", "status", "consumo_pct_disp"]],
            use_container_width=True, hide_index=True,
            column_config={
                "projeto": "Projeto",
                "area": "Área",
                "orcamento": st.column_config.NumberColumn("Orçamento (R$)", format="%.0f"),
                "realizado": st.column_config.NumberColumn("Realizado (R$)", format="%.0f"),
                "status": "Status",
                "consumo_pct_disp": st.column_config.ProgressColumn(
                    "Consumo do orçamento", min_value=0, max_value=150, format="%.0f%%"
                ),
            },
        )

    with col2:
        st.subheader("Chamados / Service Desk")
        resolvidos_total = int(tickets_f["resolvidos"].sum())
        pendentes_total = int(tickets_f["pendentes"].sum())
        em_atendimento = round(pendentes_total * 0.65)
        abertos = pendentes_total - em_atendimento
        chamados = pd.DataFrame(
            {"status": ["Resolvidos", "Em atendimento", "Abertos"], "quantidade": [resolvidos_total, em_atendimento, abertos]}
        )
        fig = px.pie(chamados, names="status", values="quantidade", hole=0.62)
        fig.update_layout(
            template="plotly_dark", height=260, margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
        a, b = st.columns(2)
        sla_medio = tickets_f["sla_pct"].mean() if not tickets_f.empty else 0
        tempo_medio = tickets_f["tempo_medio_h"].mean() if not tickets_f.empty else 0
        a.metric("SLA médio", f"{sla_medio:.0f}%")
        b.metric("Tempo médio", f"{tempo_medio:.1f}h")

    with col3:
        st.subheader("Top 5 Clientes")
        clientes = pd.DataFrame({
            "Cliente": ["GlobalTech Ltda.", "NovaCorp", "Sigma S.A.", "Alfa Comércio", "Beta Indústria"],
            "Faturamento": ["R$ 1.020.000", "R$ 780.000", "R$ 620.000", "R$ 540.000", "R$ 410.000"],
        })
        st.dataframe(clientes, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns([1.1, 1.3, 1])

    with col1:
        st.subheader("Faturamento por Região")
        fig = px.bar(regions_f.sort_values("valor"), x="valor", y="regiao", orientation="h")
        fig.update_layout(
            template="plotly_dark", height=330, margin=dict(l=5, r=5, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Evolução de Vendas")
        evolucao = monthly_f.copy()
        evolucao["meta"] = evolucao["orcamento"] * 0.90
        fig = px.line(evolucao, x="mes", y=["realizado", "meta"], markers=True)
        fig.update_layout(
            template="plotly_dark", height=330, margin=dict(l=5, r=5, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader("🚨 Alertas de Governança")
        render_alertas(projects_f, tickets_f)

# ============================================================ Financeiro ===
elif pagina == "Financeiro":
    r = resumo_financeiro(monthly_f)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Orçamento (período)", fmt_moeda(r["orcamento"]))
    k2.metric("Realizado (período)", fmt_moeda(r["realizado"]))
    k3.metric("Saldo", fmt_moeda(r["saldo"]))
    k4.metric("Tendência último mês", r["tendencia"].capitalize())

    st.markdown("###")
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Orçamento x Realizado por Mês")
        fig = px.bar(
            monthly_f, x="mes", y=["orcamento", "realizado"], barmode="group",
            labels={"value": "Valor (R$)", "variable": "", "mes": ""},
            color_discrete_sequence=["#3a4f9e", "#7c8bff"],
        )
        fig.update_layout(template="plotly_dark", height=340, margin=dict(l=10, r=10, t=20, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.plotly_chart(gauge_consumo(r["consumo"]), use_container_width=True)
        st.metric("Previsão de fechamento", fmt_moeda(r["previsao_fechamento"]))

    st.subheader("Variação Orçamento x Realizado (Waterfall)")
    fig_wf = go.Figure(
        go.Waterfall(
            x=monthly_f["mes"].astype(str),
            y=monthly_f["variacao"],
            measure=["relative"] * len(monthly_f),
            increasing={"marker": {"color": "#ff4f81"}},
            decreasing={"marker": {"color": "#26d9a3"}},
            connector={"line": {"color": "#3a4f9e"}},
        )
    )
    fig_wf.update_layout(
        template="plotly_dark", height=340, margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="Variação (R$)",
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown("<div class='glass-card'><h4>🧠 Leitura automática</h4>" + "".join(
        f"<p>• {t}</p>" for t in insights_financeiros(monthly_f)
    ) + "</div>", unsafe_allow_html=True)

# ============================================================== Projetos ===
elif pagina == "Projetos":
    status_opts = list(dados["projects"]["status"].unique())
    status_sel = st.multiselect("Status do projeto", options=status_opts, help="Deixe vazio para considerar todos os status.")
    projetos_view = filter_projects(dados["projects"], areas_sel, status_sel)

    k1, k2, k3 = st.columns(3)
    k1.metric("Projetos monitorados", len(projetos_view))
    k2.metric("Orçamento total", fmt_moeda(float(projetos_view["orcamento"].sum())) if not projetos_view.empty else "R$ 0")
    k3.metric(
        "Projetos acima do orçamento",
        int((projetos_view["consumo_pct"] > 1).sum()) if not projetos_view.empty else 0,
    )

    st.markdown("###")
    disp = projetos_view.copy()
    disp["consumo_pct_disp"] = disp["consumo_pct"] * 100
    st.dataframe(
        disp[["projeto", "area", "orcamento", "realizado", "status", "consumo_pct_disp"]],
        use_container_width=True, hide_index=True,
        column_config={
            "projeto": "Projeto",
            "area": "Área",
            "orcamento": st.column_config.NumberColumn("Orçamento (R$)", format="%.0f"),
            "realizado": st.column_config.NumberColumn("Realizado (R$)", format="%.0f"),
            "status": "Status",
            "consumo_pct_disp": st.column_config.ProgressColumn(
                "Consumo do orçamento", min_value=0, max_value=150, format="%.0f%%"
            ),
        },
    )

    if not projetos_view.empty:
        st.subheader("Orçamento x Realizado por Projeto")
        fig = px.bar(
            projetos_view, x="projeto", y=["orcamento", "realizado"], barmode="group",
            color_discrete_sequence=["#3a4f9e", "#7c8bff"],
            labels={"value": "Valor (R$)", "variable": "", "projeto": ""},
        )
        fig.update_layout(template="plotly_dark", height=340, margin=dict(l=10, r=10, t=20, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='glass-card'><h4>🧠 Leitura automática</h4>" + "".join(
        f"<p>• {t}</p>" for t in insights_projetos(projetos_view)
    ) + "</div>", unsafe_allow_html=True)

# ========================================================== Fornecedores ===
elif pagina == "Fornecedores":
    suppliers = dados["suppliers"]
    total = float(suppliers["valor"].sum())
    top = suppliers.sort_values("valor", ascending=False).iloc[0]

    k1, k2, k3 = st.columns(3)
    k1.metric("Gasto total com fornecedores", fmt_moeda(total))
    k2.metric("Principal fornecedor", top["fornecedor"])
    k3.metric("Participação do principal", fmt_pct(top["valor"] / total))

    st.markdown("###")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Distribuição de Gastos (Treemap)")
        fig = px.treemap(suppliers, path=["fornecedor"], values="valor", color="valor",
                          color_continuous_scale="Blues")
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=5, r=5, t=20, b=5),
                           paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Ranking de Fornecedores")
        fig = px.bar(suppliers.sort_values("valor"), x="valor", y="fornecedor", orientation="h")
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=5, r=5, t=20, b=5),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='glass-card'><h4>🧠 Leitura automática</h4>" + "".join(
        f"<p>• {t}</p>" for t in insights_fornecedores(suppliers)
    ) + "</div>", unsafe_allow_html=True)

# ============================================================= Contratos ===
elif pagina == "Contratos":
    contracts = dados["contracts"].sort_values("dias_para_vencer").copy()

    def _status_contrato(dias: int) -> str:
        if dias <= 30:
            return "🔴 Urgente"
        if dias <= 60:
            return "🟡 Atenção"
        return "🟢 Ok"

    contracts["status"] = contracts["dias_para_vencer"].apply(_status_contrato)
    contracts["vencimento_disp"] = contracts["vencimento"].dt.strftime("%d/%m/%Y")

    proximos = contracts[contracts["dias_para_vencer"] <= 60]
    k1, k2, k3 = st.columns(3)
    k1.metric("Contratos ativos", len(contracts))
    k2.metric("Vencendo em até 60 dias", len(proximos))
    k3.metric("Custo mensal total", fmt_moeda(float(contracts["valor_mensal"].sum())))

    st.markdown("###")
    st.dataframe(
        contracts[["fornecedor", "contrato", "vencimento_disp", "dias_para_vencer", "valor_mensal", "status"]],
        use_container_width=True, hide_index=True,
        column_config={
            "fornecedor": "Fornecedor",
            "contrato": "Contrato",
            "vencimento_disp": "Vencimento",
            "dias_para_vencer": st.column_config.NumberColumn("Dias p/ vencer"),
            "valor_mensal": st.column_config.NumberColumn("Valor mensal (R$)", format="%.0f"),
            "status": "Status",
        },
    )

    st.markdown("<div class='glass-card'><h4>🧠 Leitura automática</h4>" + "".join(
        f"<p>• {t}</p>" for t in insights_contratos(dados["contracts"])
    ) + "</div>", unsafe_allow_html=True)

# =========================================================== Service Desk ===
elif pagina == "Service Desk":
    sla_medio = tickets_f["sla_pct"].mean() if not tickets_f.empty else 0
    tempo_medio = tickets_f["tempo_medio_h"].mean() if not tickets_f.empty else 0
    total_abertos = int(tickets_f["abertos"].sum())
    total_resolvidos = int(tickets_f["resolvidos"].sum())

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Chamados abertos", total_abertos)
    k2.metric("Chamados resolvidos", total_resolvidos)
    k3.metric("Tempo médio", f"{tempo_medio:.1f}h")
    k4.metric("SLA médio", f"{sla_medio:.0f}%")

    st.markdown("###")
    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.subheader("Volume de Chamados por Mês")
        fig = px.area(
            tickets_f, x="mes", y=["abertos", "resolvidos"],
            labels={"value": "Qtd. de chamados", "variable": "", "mes": ""},
            color_discrete_sequence=["#ff7ce0", "#26d9a3"],
        )
        fig.update_layout(template="plotly_dark", height=330, margin=dict(l=10, r=10, t=20, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.plotly_chart(gauge_consumo(sla_medio / 100, titulo="SLA médio no período"), use_container_width=True)

    st.subheader("Tempo Médio de Atendimento")
    fig = px.line(tickets_f, x="mes", y="tempo_medio_h", markers=True,
                  labels={"tempo_medio_h": "Horas", "mes": ""})
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=20, b=10),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='glass-card'><h4>🧠 Leitura automática</h4>" + "".join(
        f"<p>• {t}</p>" for t in insights_service_desk(tickets_f)
    ) + "</div>", unsafe_allow_html=True)

# ================================================ Gerador de Relatórios ====
else:
    st.markdown(
        "<div class='glass-card'><h4>📄 Gerador automático de relatórios</h4>"
        "<p>Escolha o escopo do relatório abaixo. O texto é gerado automaticamente a partir "
        "dos dados e filtros aplicados no menu lateral — nada é escrito manualmente.</p></div>",
        unsafe_allow_html=True,
    )

    tipo = st.selectbox(
        "Escopo do relatório",
        ["Executivo (visão geral)", "Financeiro", "Projetos", "Fornecedores", "Service Desk", "Contratos"],
    )

    if st.button("🧠 Gerar relatório"):
        st.session_state["relatorio_tipo_gerado"] = tipo

    if st.session_state.get("relatorio_tipo_gerado") == tipo:
        if tipo.startswith("Executivo"):
            titulo = "Relatorio Executivo - TechCore IT Analytics"
            secoes = {
                "Financeiro": insights_financeiros(monthly_f),
                "Projetos": insights_projetos(projects_f),
                "Fornecedores": insights_fornecedores(dados["suppliers"]),
                "Service Desk": insights_service_desk(tickets_f),
                "Contratos": insights_contratos(dados["contracts"]),
            }
        elif tipo == "Financeiro":
            titulo = "Relatorio Financeiro - TechCore IT Analytics"
            secoes = {"Financeiro": insights_financeiros(monthly_f)}
        elif tipo == "Projetos":
            titulo = "Relatorio de Projetos - TechCore IT Analytics"
            secoes = {"Projetos": insights_projetos(projects_f)}
        elif tipo == "Fornecedores":
            titulo = "Relatorio de Fornecedores - TechCore IT Analytics"
            secoes = {"Fornecedores": insights_fornecedores(dados["suppliers"])}
        elif tipo == "Service Desk":
            titulo = "Relatorio de Service Desk - TechCore IT Analytics"
            secoes = {"Service Desk": insights_service_desk(tickets_f)}
        else:
            titulo = "Relatorio de Contratos - TechCore IT Analytics"
            secoes = {"Contratos": insights_contratos(dados["contracts"])}

        st.markdown("#### 📋 Prévia do relatório")
        for nome_secao, textos in secoes.items():
            st.markdown(f"**{nome_secao}**")
            for t in textos:
                st.markdown(f"- {t}")

        md = montar_relatorio_markdown(titulo, secoes)
        pdf_bytes = montar_relatorio_pdf(titulo, secoes)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "⬇️ Baixar em Markdown", data=md, file_name="relatorio_techcore.md",
                mime="text/markdown", use_container_width=True,
            )
        with c2:
            st.download_button(
                "⬇️ Baixar em PDF", data=pdf_bytes, file_name="relatorio_techcore.pdf",
                mime="application/pdf", use_container_width=True,
            )
    else:
        st.info("Clique em **Gerar relatório** para criar a análise automática com base nos filtros atuais.")

st.markdown("---")
st.caption("Projeto fictício • TechCore Solutions • Dados simulados para portfólio")
