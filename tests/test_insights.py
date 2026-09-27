"""Testes unitários do motor de insights (src/insights.py).

Executar com: pytest -q
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.insights import (  # noqa: E402
    fmt_moeda,
    fmt_pct,
    insights_contratos,
    insights_financeiros,
    insights_fornecedores,
    insights_projetos,
    insights_service_desk,
    resumo_financeiro,
)


def _monthly_df() -> pd.DataFrame:
    df = pd.DataFrame({
        "mes": ["Jan", "Fev", "Mar"],
        "orcamento": [1000, 1000, 1000],
        "realizado": [900, 950, 1100],
    })
    df["variacao"] = df["realizado"] - df["orcamento"]
    df["consumo_pct"] = df["realizado"] / df["orcamento"]
    return df


def test_fmt_moeda_padrao_brasileiro():
    assert fmt_moeda(1234567) == "R$ 1.234.567"


def test_fmt_pct_padrao_brasileiro():
    assert fmt_pct(0.925) == "92,5%"


def test_resumo_financeiro_calcula_saldo_e_consumo():
    r = resumo_financeiro(_monthly_df())
    assert r["orcamento"] == 3000
    assert r["realizado"] == 2950
    assert r["saldo"] == 50
    assert round(r["consumo"], 4) == round(2950 / 3000, 4)


def test_insights_financeiros_detecta_estouro():
    textos = insights_financeiros(_monthly_df())
    assert any("Mar" in t for t in textos)


def test_insights_projetos_detecta_estouro():
    projetos = pd.DataFrame({
        "projeto": ["A", "B"],
        "area": ["Infraestrutura", "Sistemas"],
        "orcamento": [100, 200],
        "realizado": [90, 250],
        "status": ["Em andamento", "Acima do orçamento"],
    })
    projetos["consumo_pct"] = projetos["realizado"] / projetos["orcamento"]
    textos = insights_projetos(projetos)
    assert any("B" in t for t in textos)


def test_insights_projetos_vazio():
    vazio = pd.DataFrame(columns=["projeto", "area", "orcamento", "realizado", "status", "consumo_pct"])
    textos = insights_projetos(vazio)
    assert len(textos) == 1


def test_insights_fornecedores_identifica_concentracao():
    fornecedores = pd.DataFrame({"fornecedor": ["X", "Y"], "valor": [900, 100]})
    textos = insights_fornecedores(fornecedores)
    assert any("X" in t for t in textos)
    assert any("elevada" in t for t in textos)


def test_insights_service_desk_abaixo_da_meta():
    tickets = pd.DataFrame({
        "mes": ["Jan", "Fev"],
        "abertos": [100, 100],
        "resolvidos": [70, 75],
        "sla_pct": [80, 82],
        "tempo_medio_h": [5.0, 4.8],
    })
    tickets["pendentes"] = tickets["abertos"] - tickets["resolvidos"]
    textos = insights_service_desk(tickets)
    assert any("abaixo da meta" in t for t in textos)


def test_insights_contratos_sem_vencimento_proximo():
    contratos = pd.DataFrame({"contrato": ["C1"], "dias_para_vencer": [200]})
    textos = insights_contratos(contratos)
    assert "Nenhum contrato" in textos[0]
