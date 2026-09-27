"""Camada de acesso e preparação de dados do TechCore IT Analytics.

Centraliza a leitura dos CSVs, o cache de carregamento e as funções de
filtragem usadas pelas páginas do dashboard.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

MESES_ORDEM = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


@st.cache_data(show_spinner=False)
def load_all() -> dict[str, pd.DataFrame]:
    """Carrega e prepara todos os datasets do projeto (com cache de dados)."""
    monthly = pd.read_csv(DATA_DIR / "orcamento_mensal.csv")
    monthly["mes"] = pd.Categorical(monthly["mes"], categories=MESES_ORDEM, ordered=True)
    monthly = monthly.sort_values("mes").reset_index(drop=True)
    monthly["variacao"] = monthly["realizado"] - monthly["orcamento"]
    monthly["consumo_pct"] = monthly["realizado"] / monthly["orcamento"]

    projects = pd.read_csv(DATA_DIR / "projetos.csv")
    projects["consumo_pct"] = projects["realizado"] / projects["orcamento"]

    areas = pd.read_csv(DATA_DIR / "custos_area.csv")
    suppliers = pd.read_csv(DATA_DIR / "custos_fornecedor.csv")
    regions = pd.read_csv(DATA_DIR / "faturamento_regiao.csv")

    contracts = pd.read_csv(DATA_DIR / "contratos.csv", parse_dates=["inicio", "vencimento"])
    hoje = pd.Timestamp(dt.date.today())
    contracts["dias_para_vencer"] = (contracts["vencimento"] - hoje).dt.days

    tickets = pd.read_csv(DATA_DIR / "chamados_mensal.csv")
    tickets["mes"] = pd.Categorical(tickets["mes"], categories=MESES_ORDEM, ordered=True)
    tickets = tickets.sort_values("mes").reset_index(drop=True)
    tickets["pendentes"] = tickets["abertos"] - tickets["resolvidos"]

    return {
        "monthly": monthly,
        "projects": projects,
        "areas": areas,
        "suppliers": suppliers,
        "regions": regions,
        "contracts": contracts,
        "tickets": tickets,
    }


def filter_monthly(monthly: pd.DataFrame, mes_ini: str, mes_fim: str) -> pd.DataFrame:
    """Filtra o dataframe mensal para o intervalo de meses selecionado."""
    i0, i1 = MESES_ORDEM.index(mes_ini), MESES_ORDEM.index(mes_fim)
    meses_sel = MESES_ORDEM[i0 : i1 + 1]
    return monthly[monthly["mes"].isin(meses_sel)].copy()


def filter_tickets(tickets: pd.DataFrame, mes_ini: str, mes_fim: str) -> pd.DataFrame:
    """Filtra o dataframe de chamados para o intervalo de meses selecionado."""
    return filter_monthly(tickets, mes_ini, mes_fim)


def filter_projects(projects: pd.DataFrame, areas_sel: list[str], status_sel: list[str]) -> pd.DataFrame:
    """Filtra projetos por área e por status."""
    df = projects.copy()
    if areas_sel:
        df = df[df["area"].isin(areas_sel)]
    if status_sel:
        df = df[df["status"].isin(status_sel)]
    return df


def filter_regions(regions: pd.DataFrame, regioes_sel: list[str]) -> pd.DataFrame:
    """Filtra faturamento por região."""
    if not regioes_sel:
        return regions.copy()
    return regions[regions["regiao"].isin(regioes_sel)].copy()


def filter_areas(areas: pd.DataFrame, areas_sel: list[str]) -> pd.DataFrame:
    """Filtra custos por área."""
    if not areas_sel:
        return areas.copy()
    return areas[areas["area"].isin(areas_sel)].copy()
