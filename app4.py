import dash
from dash import dcc, html, Input, Output, ctx
import pandas as pd
import webbrowser
import threading

# Inicializa app
app = dash.Dash(__name__)

# DataFrame inicial
dados = pd.DataFrame(columns=["Estatística", "Quantidade"])

# Lista de estatísticas (para mapear botões)
estatisticas = {
    "btn-chutes": "Chutes a Gol",
    "btn-fora": "Chute pra Fora",
    "btn-gols": "Gols",
    "btn-escanteios": "Escanteios",
    "btn-cruzamento": "Cruzamento na Área",
    "btn-lancamento": "Lançamento Profundidade",
    "btn-virada": "Virada de Jogo",
    "btn-defesas": "Defesas Goleiro",
    "btn-desarmes": "Desarmes",
    "btn-posse": "Posse de Bola",
    "btn-passes": "Passes Certos",
    "btn-passes-errados": "Passes Errados",
    "btn-faltas": "Faltas Cometidas",
    "btn-amarelo": "Cartão Amarelo",
    "btn-vermelho": "Cartão Vermelho"
    
}

# Estilo padrão dos botões (maiores e mais fáceis de clicar)
botao_estilo = {
    "padding": "15px 25px",
    "fontSize": "18px",
    "fontWeight": "bold",
    "borderRadius": "10px",
    "cursor": "pointer",
    "minWidth": "200px"
}


# Layout
app.layout = html.Div([
    # Logo + título
    html.Div([
        html.Img(src="/assets/logo.png", style={"width": "120px", "margin": "10px auto", "display": "block"}),
        html.H1("Dashboard Estatísticas de Jogo", style={"textAlign": "center"})
    ]),

  


    # Grupo Ataque
    html.Div([
        html.H3("⚽ Ataque"),
        html.Div([
            html.Button("Chutes a Gol", id="btn-chutes", n_clicks=0, style={**botao_estilo, "background": "#28a745", "color": "white"}),
            html.Button("Chute pra Fora", id="btn-fora", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"}),
            html.Button("Gols", id="btn-gols", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"}),
            html.Button("Escanteios", id="btn-escanteios", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"}),
            html.Button("Cruzamento na Área", id="btn-cruzamento", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"}),
            html.Button("Lançamento Profundidade", id="btn-lancamento", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"}),
            html.Button("Virada de Jogo", id="btn-virada", n_clicks=0, style={**botao_estilo,"background": "#28a745", "color": "white"})
        ], style={"display": "flex", "flex-wrap": "wrap", "gap": "10px"})
    ]),

    # Grupo Defesa
    html.Div([
        html.H3("🛡️ Defesa"),
        html.Div([
            html.Button("Defesas Goleiro", id="btn-defesas", n_clicks=0, style={**botao_estilo,"background": "#007bff", "color": "white"}),
            html.Button("Desarmes", id="btn-desarmes", n_clicks=0, style={**botao_estilo,"background": "#007bff", "color": "white"}),
            html.Button("Posse de Bola", id="btn-posse", n_clicks=0, style={**botao_estilo,"background": "#007bff", "color": "white"})
        ], style={"display": "flex", "flex-wrap": "wrap", "gap": "10px"})
    ]),

    # Grupo Disputa
    html.Div([
        html.H3("🏃 Disputa"),
        html.Div([
            html.Button("Passes Certos", id="btn-passes", n_clicks=0, style={**botao_estilo,"background": "#fd7e14", "color": "white"}),
            html.Button("Passes Errados", id="btn-passes-errados", n_clicks=0, style={**botao_estilo,"background": "#d10b0b", "color": "white"}),
            html.Button("Faltas Cometidas", id="btn-faltas", n_clicks=0, style={**botao_estilo,"background": "#fd7e14", "color": "white"})
        ], style={"display": "flex", "flex-wrap": "wrap", "gap": "10px"})
    ]),

    # Grupo Disciplina
    html.Div([
        html.H3("🚨 Disciplina"),
        html.Div([
            html.Button("Cartão Amarelo", id="btn-amarelo", n_clicks=0, style={**botao_estilo,"background": "#ffc107", "color": "black"}),
            html.Button("Cartão Vermelho", id="btn-vermelho", n_clicks=0, style={**botao_estilo,"background": "#dc3545", "color": "white"})
        ], style={"display": "flex", "flex-wrap": "wrap", "gap": "10px"})
    ]),

    # Tabela
    html.Div([
        html.H3("📊 Tabela de Estatísticas"),
        html.Div(id="tabela")
    ]),

    # Gráfico
    html.Div([
        dcc.Graph(id="grafico")
    ]),

    # Botão download
    html.Div([
        html.Button("📥 Baixar CSV", id="btn-download"),
        dcc.Download(id="download-dataframe-csv")
    ], style={"textAlign": "center", "margin": "20px"})
])

# Callback para atualizar tabela e gráfico
@app.callback(
    [Output("tabela", "children"),
     Output("grafico", "figure")],
    [Input(btn_id, "n_clicks") for btn_id in estatisticas.keys()],
    prevent_initial_call=True
)
def atualizar_tabela(*args):
    global dados
    # Identifica qual botão foi clicado
    if not ctx.triggered_id:
        return dash.no_update, dash.no_update

    estatistica_clicada = estatisticas.get(ctx.triggered_id)

    if estatistica_clicada:
        if estatistica_clicada in dados["Estatística"].values:
            dados.loc[dados["Estatística"] == estatistica_clicada, "Quantidade"] += 1
        else:
            dados.loc[len(dados)] = [estatistica_clicada, 1]

    # Monta tabela
    tabela = html.Table([
        html.Thead(html.Tr([html.Th("Estatística"), html.Th("Quantidade")])),
        html.Tbody([html.Tr([html.Td(row["Estatística"]), html.Td(row["Quantidade"])]) for _, row in dados.iterrows()])
    ], style={"width": "100%", "textAlign": "center"})

    # Monta gráfico
    figura = {
        "data": [{"x": dados["Estatística"], "y": dados["Quantidade"], "type": "bar", "marker": {"color": "orange"}}],
        "layout": {
            "title": "Estatísticas Registradas",
            "paper_bgcolor": "#111",
            "plot_bgcolor": "#111",
            "font": {"color": "white"}
        }
    }
    return tabela, figura

# Callback para baixar CSV
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    return dcc.send_data_frame(dados.to_csv, "estatisticas_jogo.csv", index=False, sep=";")

# Abre navegador automaticamente
if __name__ == "__main__":
    def abrir_navegador():
        webbrowser.open_new("http://127.0.0.1:8050/")

    threading.Timer(1, abrir_navegador).start()
    app.run(debug=False)
