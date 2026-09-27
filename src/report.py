"""Geração de relatórios (Markdown e PDF) a partir dos insights calculados.

Este módulo é o "gerador de relatórios" do TechCore IT Analytics: recebe um
dicionário {seção: [insights]} e produz tanto um Markdown quanto um PDF
prontos para download, sem nenhuma dependência do Streamlit.
"""
from __future__ import annotations

import datetime as dt
import unicodedata

from fpdf import FPDF

NOME_APP = "TechCore IT Analytics"


def montar_relatorio_markdown(titulo: str, secoes: dict[str, list[str]]) -> str:
    """Monta um relatório em Markdown a partir das seções de insights."""
    linhas = [
        f"# {titulo}",
        "",
        f"_Gerado em {dt.date.today().strftime('%d/%m/%Y')} • {NOME_APP}_",
        "",
    ]
    for nome_secao, textos in secoes.items():
        linhas.append(f"## {nome_secao}")
        linhas.append("")
        for t in textos:
            linhas.append(f"- {t}")
        linhas.append("")
    linhas.append("---")
    linhas.append("_Relatório gerado automaticamente a partir de dados fictícios, para fins de portfólio._")
    return "\n".join(linhas)


def _quebrar_palavras_longas(texto: str, tamanho_max: int = 45) -> str:
    """Insere espaços dentro de 'palavras' muito longas (sem espaços) para
    garantir que o fpdf2 sempre consiga quebrar a linha. Isso evita o erro
    'Not enough horizontal space to render a single character', que ocorre
    quando um token sem quebra é maior que a largura disponível."""
    palavras = texto.split(" ")
    corrigidas = [
        " ".join(p[i : i + tamanho_max] for i in range(0, len(p), tamanho_max)) if len(p) > tamanho_max else p
        for p in palavras
    ]
    return " ".join(corrigidas)


def _pdf_safe(texto: str) -> str:
    """Garante que o texto seja compatível com a codificação latin-1 usada
    pelas fontes core do PDF e que não existam tokens longos demais."""
    normalizado = unicodedata.normalize("NFKC", _quebrar_palavras_longas(texto))
    return normalizado.encode("latin-1", "replace").decode("latin-1")


class _RelatorioPDF(FPDF):
    def header(self) -> None:
        largura = self.epw
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 30, 70)
        self.cell(largura, 10, NOME_APP, ln=1)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(110, 110, 130)
        self.cell(largura, 6, f"Gerado em {dt.date.today().strftime('%d/%m/%Y')}", ln=1)
        self.ln(2)
        self.set_draw_color(200, 200, 210)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 160)
        self.cell(self.epw, 10, f"Pagina {self.page_no()}", align="C")


def _linha_pdf(pdf: FPDF, texto: str, altura: float = 7) -> None:
    """Escreve uma linha de texto usando SEMPRE uma largura explícita
    (pdf.epw) e o cursor reposicionado na margem esquerda. Isso evita
    depender do cálculo automático de largura (w=0), que é a causa raiz do
    FPDFException disparado ao atravessar uma quebra de página no meio de
    um texto longo."""
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, altura, _pdf_safe(texto))


def montar_relatorio_pdf(titulo: str, secoes: dict[str, list[str]]) -> bytes:
    """Monta um relatório em PDF a partir das seções de insights."""
    pdf = _RelatorioPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 30, 70)
    _linha_pdf(pdf, titulo, altura=10)
    pdf.ln(2)

    for nome_secao, textos in secoes.items():
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 60, 140)
        _linha_pdf(pdf, nome_secao, altura=9)

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 50)
        for t in textos:
            _linha_pdf(pdf, f"- {t}", altura=7)
        pdf.ln(3)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(130, 130, 140)
    _linha_pdf(pdf, "Relatorio gerado automaticamente a partir de dados ficticios, para fins de portfolio.", altura=6)

    saida = pdf.output(dest="S")
    return bytes(saida)
