"""Motor de insights do TechCore IT Analytics.

Funções puras (sem dependência do Streamlit) que recebem dataframes já
filtrados e devolvem textos analíticos em português, prontos para serem
exibidos na tela ou incluídos em um relatório exportável.
"""
from __future__ import annotations

import pandas as pd


def fmt_moeda(v: float) -> str:
    """Formata um número como moeda no padrão brasileiro (R$ 1.234.567)."""
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(v: float) -> str:
    """Formata uma fração (0.925) como percentual no padrão brasileiro (92,5%)."""
    return f"{v * 100:.1f}%".replace(".", ",")


def resumo_financeiro(monthly: pd.DataFrame) -> dict:
    """Calcula os principais indicadores financeiros a partir do dataframe mensal."""
    orcamento = float(monthly["orcamento"].sum())
    realizado = float(monthly["realizado"].sum())
    saldo = orcamento - realizado
    consumo = realizado / orcamento if orcamento else 0.0
    tendencia = "estável"
    if len(monthly) >= 2:
        delta = monthly["realizado"].iloc[-1] - monthly["realizado"].iloc[-2]
        tendencia = "em alta" if delta > 0 else "em queda" if delta < 0 else "estável"
    n_meses = max(len(monthly), 1)
    ritmo_mensal = realizado / n_meses
    meses_restantes = 12 - n_meses
    previsao_fechamento = realizado + ritmo_mensal * max(meses_restantes, 0)
    return {
        "orcamento": orcamento,
        "realizado": realizado,
        "saldo": saldo,
        "consumo": consumo,
        "tendencia": tendencia,
        "previsao_fechamento": previsao_fechamento,
    }


def insights_financeiros(monthly: pd.DataFrame) -> list[str]:
    """Gera insights textuais sobre orçamento x realizado."""
    if monthly.empty:
        return ["Não há dados financeiros para o período selecionado."]

    r = resumo_financeiro(monthly)
    textos = [
        f"No período selecionado, o orçamento de TI é de {fmt_moeda(r['orcamento'])}, "
        f"com {fmt_moeda(r['realizado'])} já realizados ({fmt_pct(r['consumo'])} do total).",
        f"O saldo disponível é de {fmt_moeda(r['saldo'])} e a tendência do último mês "
        f"analisado é {r['tendencia']}.",
        f"Mantendo o ritmo atual de gastos, a previsão de fechamento do período é de "
        f"aproximadamente {fmt_moeda(r['previsao_fechamento'])}.",
    ]

    if r["consumo"] > 0.95:
        textos.append(
            "O consumo orçamentário está próximo do limite planejado - recomenda-se "
            "atenção redobrada aos próximos lançamentos e uma revisão de contratos em aberto."
        )
    elif r["consumo"] < 0.6:
        textos.append(
            "O ritmo de execução orçamentária está abaixo do esperado para o período, "
            "o que pode indicar atrasos em projetos, contratações ou faturamento de fornecedores."
        )
    else:
        textos.append(
            "O ritmo de consumo orçamentário está dentro de uma faixa saudável para o período analisado."
        )

    meses_estouro = monthly[monthly["variacao"] > 0]
    if not meses_estouro.empty:
        pior = meses_estouro.sort_values("variacao", ascending=False).iloc[0]
        textos.append(
            f"O mês de {pior['mes']} apresentou o maior estouro orçamentário do período, "
            f"com {fmt_moeda(pior['variacao'])} acima do planejado."
        )

    return textos


def insights_projetos(projects: pd.DataFrame) -> list[str]:
    """Gera insights textuais sobre a carteira de projetos de TI."""
    total = len(projects)
    if total == 0:
        return ["Nenhum projeto encontrado para os filtros selecionados."]

    estourados = projects[projects["consumo_pct"] > 1]
    concluidos = projects[projects["status"].str.contains("Conclu", case=False, na=False)]
    textos = [
        f"Há {total} projeto(s) monitorado(s) nos filtros atuais, sendo {len(concluidos)} concluído(s)."
    ]

    if not estourados.empty:
        nomes = ", ".join(estourados["projeto"].tolist())
        textos.append(f"{len(estourados)} projeto(s) ultrapassaram o orçamento previsto: {nomes}.")
    else:
        textos.append("Nenhum projeto ultrapassou o orçamento previsto - bom sinal de controle de custos.")

    maior = projects.sort_values("orcamento", ascending=False).iloc[0]
    textos.append(
        f"O projeto de maior orçamento é '{maior['projeto']}', da área de {maior['area']}, "
        f"com {fmt_moeda(float(maior['orcamento']))} previstos."
    )
    return textos


def insights_fornecedores(suppliers: pd.DataFrame) -> list[str]:
    """Gera insights textuais sobre concentração de gastos com fornecedores."""
    if suppliers.empty:
        return ["Nenhum fornecedor encontrado para os filtros selecionados."]

    total = float(suppliers["valor"].sum())
    top = suppliers.sort_values("valor", ascending=False).iloc[0]
    participacao = top["valor"] / total if total else 0.0

    textos = [
        f"O gasto total com fornecedores no período é de {fmt_moeda(total)}.",
        f"O fornecedor '{top['fornecedor']}' concentra {fmt_pct(participacao)} do gasto total, "
        f"sendo o principal ponto de atenção em negociações contratuais.",
    ]
    if participacao > 0.3:
        textos.append(
            "A concentração de gastos em um único fornecedor é elevada - vale avaliar "
            "estratégias de diversificação para reduzir o risco de dependência."
        )
    return textos


def insights_service_desk(tickets: pd.DataFrame) -> list[str]:
    """Gera insights textuais sobre o desempenho do Service Desk."""
    if tickets.empty:
        return ["Não há dados de Service Desk para o período selecionado."]

    sla_medio = float(tickets["sla_pct"].mean())
    tempo_medio = float(tickets["tempo_medio_h"].mean())
    pendentes = int(tickets["pendentes"].sum())

    textos = [
        f"O SLA médio do período é de {sla_medio:.1f}%, com tempo médio de atendimento "
        f"de {tempo_medio:.1f} horas.",
    ]
    if sla_medio >= 90:
        textos.append("O nível de serviço está dentro da meta esperada (acima de 90%).")
    else:
        textos.append(
            "O SLA médio está abaixo da meta de 90% - recomenda-se revisão da capacidade "
            "da equipe de suporte ou dos processos de triagem."
        )
    textos.append(f"Há um saldo acumulado de {pendentes} chamados pendentes no período analisado.")
    return textos


def insights_contratos(contracts: pd.DataFrame, limite_dias: int = 60) -> list[str]:
    """Gera insights textuais sobre contratos próximos do vencimento."""
    if contracts.empty:
        return ["Nenhum contrato cadastrado."]

    proximos = contracts[contracts["dias_para_vencer"] <= limite_dias]
    if proximos.empty:
        return [f"Nenhum contrato vence nos próximos {limite_dias} dias."]

    nomes = ", ".join(proximos.sort_values("dias_para_vencer")["contrato"].tolist())
    return [
        f"{len(proximos)} contrato(s) vencem nos próximos {limite_dias} dias: {nomes}. "
        f"Recomenda-se iniciar as tratativas de renovação ou nova licitação."
    ]


def gerar_resumo_executivo(dados: dict) -> list[str]:
    """Combina os principais insights de todas as frentes em um resumo executivo único."""
    textos: list[str] = []
    textos += insights_financeiros(dados["monthly"])
    textos += insights_projetos(dados["projects"])
    textos += insights_fornecedores(dados["suppliers"])
    textos += insights_service_desk(dados["tickets"])
    textos += insights_contratos(dados["contracts"])
    return textos
