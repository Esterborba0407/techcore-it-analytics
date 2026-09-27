#  TechCore IT Analytics

O **TechCore IT Analytics** é um projeto de portfólio que desenvolvi para colocar em prática meus conhecimentos em **Python, análise de dados e Governança de TI**.

A ideia surgiu de uma situação que faz parte da minha experiência profissional: trabalhar com **orçamento, projetos, fornecedores, contratos, indicadores e processos de TI** e perceber que, muitas vezes, não basta apenas visualizar os números. É preciso transformar esses dados em informações que realmente ajudem na tomada de decisão.

Por isso, decidi ir além de um dashboard tradicional.

Em vez de criar apenas gráficos e indicadores, desenvolvi um dashboard que também **analisa os dados e gera insights automaticamente**.

> **Importante:** este é um projeto fictício. Todos os dados utilizados foram criados exclusivamente para fins de estudo e portfólio, sem utilização de informações reais ou confidenciais de empresas.

---

##  O que eu desenvolvi

O projeto simula uma solução de **Analytics para Governança e Gestão de TI**, reunindo informações financeiras, operacionais e de serviços em um único ambiente.

Durante o desenvolvimento, trabalhei desde o tratamento dos dados até a construção da interface, regras de negócio, geração de relatórios e testes automatizados.

O dashboard possui **7 áreas de análise**:

*  Visão Geral
* Financeiro
*  Projetos
*  Fornecedores
*  Contratos
* Service Desk
* Gerador de Relatórios

---

##  Do dashboard para a análise automática

Essa foi uma das partes que mais gostei de desenvolver.

Eu não queria que o projeto fosse apenas um conjunto de gráficos mostrando números. Queria que ele conseguisse **interpretar algumas situações a partir dos próprios dados**.

Para isso, criei um motor de insights baseado em **regras de negócio**.

Por exemplo, dependendo dos dados filtrados, o sistema pode identificar situações como:

* orçamento acima do planejado;
* concentração de gastos em determinados fornecedores;
* SLA abaixo da meta;
* contratos próximos do vencimento;
* variações relevantes no orçamento;
* indicadores que precisam de atenção.

A partir dessas regras, o sistema transforma os resultados em **textos analíticos em português**.

Assim, em vez de apenas mostrar:

> Consumo do orçamento: 87%

o sistema consegue gerar uma análise contextualizada sobre aquele indicador.

---

##  Gerador automático de relatórios

Também desenvolvi um **Gerador de Relatórios** integrado ao dashboard.

A pessoa pode aplicar os filtros desejados, escolher o tipo de análise e gerar automaticamente um relatório com base nos dados daquele momento.

Os relatórios podem ser gerados em:

* **Markdown**
* **PDF**

Os escopos disponíveis são:

* Executivo
* Financeiro
* Projetos
* Fornecedores
* Service Desk
* Contratos

O objetivo foi transformar o dashboard em algo mais próximo de uma ferramenta utilizada no dia a dia de uma área de TI, onde os dados não ficam apenas na tela, mas também podem ser utilizados para gerar uma análise executiva.

---

##  Filtros dinâmicos

Outro ponto importante do projeto foi fazer com que os filtros realmente impactassem toda a análise.

É possível filtrar por:

*  Período
*  Região
* Área de TI

Os filtros são aplicados aos **KPIs, gráficos, tabelas, alertas e relatórios**.

Dessa forma, quando altero um filtro, os resultados apresentados no dashboard são recalculados de acordo com aquele contexto.

---

## Visualizações

Para apresentar os dados de forma mais clara, utilizei diferentes tipos de visualização, como:

* velocímetro (*gauge*) para consumo orçamentário;
* velocímetro de SLA;
* gráfico *waterfall* para variação do orçamento;
* *treemap* para concentração de gastos por fornecedor;
* gráficos de acompanhamento de projetos;
* indicadores e tabelas interativas.

A escolha das visualizações foi pensada de acordo com o tipo de informação que precisava ser analisada, e não apenas para deixar o dashboard visualmente bonito.

---

## 🎨 Interface

Também quis trabalhar a parte visual do projeto.

Criei uma interface própria com:

* tema escuro;
* gradientes;
* cartões com efeito *glassmorphism*;
* tipografia personalizada;
* indicadores de status;
* microinterações;
* organização visual voltada para uma experiência mais próxima de um sistema corporativo.

A ideia foi tentar equilibrar **informação, usabilidade e apresentação visual**.

---

## 🧪 Testes automatizados

Além de desenvolver a interface, também comecei a aplicar uma preocupação importante no desenvolvimento de software: **testar a lógica de negócio**.

Criei testes utilizando `pytest` para validar o funcionamento do motor de insights.

Isso permite verificar se as regras estão retornando os resultados esperados e ajuda a evitar que alterações futuras quebrem funcionalidades existentes.

---

## 🏗️ Estrutura do projeto

Organizei o projeto separando a interface da lógica de negócio e do tratamento dos dados:

```text
techcore_it_analytics/
│
├── app.py
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   ├── data_loader.py
│   ├── insights.py
│   ├── report.py
│   └── styles.py
│
├── data/
│   ├── orcamento_mensal.csv
│   ├── projetos.csv
│   ├── custos_area.csv
│   ├── custos_fornecedor.csv
│   ├── faturamento_regiao.csv
│   ├── contratos.csv
│   └── chamados_mensal.csv
│
└── tests/
    └── test_insights.py
```

Uma das preocupações durante o desenvolvimento foi não deixar toda a lógica dentro do `app.py`.

Por isso, organizei as responsabilidades em diferentes módulos:

* `data_loader.py` → carregamento, tratamento e filtros dos dados;
* `insights.py` → regras de negócio e geração dos insights;
* `report.py` → geração dos relatórios;
* `styles.py` → personalização visual;
* `app.py` → interface e organização das páginas;
* `tests/` → testes automatizados.

Isso deixa o projeto mais organizado e facilita sua manutenção e evolução.

---

## 🔄 Como funciona

De forma simplificada, o fluxo do projeto funciona assim:

```text
Dados fictícios
      ↓
Tratamento com Pandas
      ↓
Filtros aplicados pelo usuário
      ↓
Indicadores e visualizações
      ↓
Regras de negócio
      ↓
Insights automáticos
      ↓
Relatório em Markdown ou PDF
```

Ou seja, a ideia não é apenas **mostrar o dado**, mas criar uma pequena camada de análise sobre ele.

---

## 🛠️ Tecnologias utilizadas

**Desenvolvimento e dados**

* Python
* Pandas
* Streamlit
* Plotly

**Relatórios**

* fpdf2
* Markdown

**Qualidade**

* pytest

---

## 🚀 Como executar o projeto

Clone o repositório e crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No macOS/Linux:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
streamlit run app.py
```

Para executar os testes:

```bash
pytest -q
```

---

## 🎯 O que eu busquei desenvolver com esse projeto

Mais do que criar um dashboard bonito, meu objetivo foi **aprender fazendo** e juntar conhecimentos que venho desenvolvendo em diferentes áreas.

Como tenho experiência com **Finanças e Governança de TI**, usei esse conhecimento para pensar nas regras de negócio e na estrutura dos indicadores.

Ao mesmo tempo, utilizei meus conhecimentos de programação e dados para transformar essas necessidades em uma aplicação funcional.

Esse projeto me ajudou a aprofundar principalmente em:

* análise e tratamento de dados;
* Python;
* desenvolvimento de dashboards;
* criação de regras de negócio;
* automação de análises;
* geração de relatórios;
* testes automatizados;
* organização de projetos;
* visualização de dados.

---

## 💡 Por que criei esse projeto?

Minha intenção foi mostrar que **dados não precisam servir apenas para criar gráficos**.

Quando combinamos dados, regras de negócio e automação, conseguimos criar ferramentas que ajudam a transformar números em informações mais fáceis de interpretar.

Foi justamente essa ideia que tentei colocar em prática no **TechCore IT Analytics**:

> **Transformar dados de TI em informações que possam apoiar a análise e a tomada de decisão.**

---

### 👩‍💻 Sobre mim

Sou estudante de **Engenharia de Software** e venho construindo minha trajetória unindo conhecimentos de **Tecnologia, Finanças, Governança de TI, Dados e Automação**.

Gosto de entender um problema de negócio, analisar como ele funciona e pensar em como a tecnologia pode ajudar a tornar aquele processo mais eficiente.

Este projeto é parte desse processo de aprendizado e evolução profissional.

**Desenvolvido por Ester Santos da Cruz Borba.**

---

*Projeto desenvolvido exclusivamente para fins de estudo e portfólio. Todos os dados apresentados são fictícios.*
