import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

from constants import MODELS, SIDEBAR_STYLE
import os

# to get the current working directory
directory = os.getcwd()
subdir = os.path.join(directory, "mydash")
load_figure_template("LUX")


# ----------------------- VARIABLE -----------------------

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True
)


sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P("Choose a filter", className="lead"),
        dbc.Nav(
            [
                dcc.Dropdown(
                    id="Type_of_research",
                    options=[{"label": MODELS, "value": MODELS}],
                    placeholder="Select a type of research",
                ),
                html.Br(),
                dcc.Dropdown(id="filter"),
                # html.Br(),
                # dbc.Button("Add Chart", id="button"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

f_1_data = pd.read_csv(os.path.join(subdir, "f1_data.csv"))

dict_of_data = {MODELS: f_1_data}

# ---------------------------------- HELPERS


@app.callback(Output("filter", "options"), Input("Type_of_research", "value"))
def change_dropdown(type_of_research):
    if type_of_research is None:
        return [{"label": "", "value": ""}]
    if type_of_research == MODELS:
        return [
            {"label": "Bag-of-words", "value": "BoW"},
            {"label": "Word2vec", "value": "W2V"},
            {"label": "DistilBERT", "value": "DB"},
            {"label": "All", "value": ""},
        ]


@app.callback(Output("output", "figure"), Input("filter", "value"))
def plot_data(filter):
    fig = go.Figure()
    data_to_plot = f_1_data[f_1_data["name-method"].str.contains(str(filter))]
    fig.add_bar(x=data_to_plot["name-method"], y=data_to_plot["f1-score-weighted"])

    if filter == "":
        title = "F1-score-weighted for all models"
    elif filter is not None:
        title = f"F1-score-weighted for models based on {filter}"
    else:
        title = ""

    fig.layout.title = title
    fig.layout.template = "simple_white"

    print(fig)

    return fig


# ---------------------------------------


# ----------------------- DASH APP -----------------------


app.layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(),
                dbc.Col(
                    [
                        html.H1(
                            "Amazon Fine Food Reviews", style={"textAlign": "center"}
                        ),
                        html.H2(
                            "Sentiment Analysis from BoW to DistilBERT Transformers",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    [
                                        dcc.Graph(
                                            id="output",
                                            style={"width": "99%", "height": "50%"},
                                        )
                                    ]
                                ),
                            ],
                            style={"margin-top": "5%", "margin-left": "-100px"},
                        ),
                        html.Br(),  # spacing
                    ],
                    width=9,
                    style={"margin-left": "7px", "margin-top": "7px"},
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            [
                                                html.Ul(
                                                    [
                                                        html.Br(),
                                                        html.Li(
                                                            "Number of Economies: 170"
                                                        ),
                                                        html.Li(
                                                            "Temporal Coverage: 1974 - 2019"
                                                        ),
                                                        html.Li(
                                                            "Update Frequency: Quarterly"
                                                        ),
                                                        html.Li(
                                                            "Last Updated: March 18, 2020"
                                                        ),
                                                        html.Li(
                                                            [
                                                                "Source: ",
                                                                html.A(
                                                                    "https://datacatalog.worldbank.org/dataset/poverty-and-equity-database",
                                                                    href="https://datacatalog.worldbank.org/dataset/poverty-and-equity-database",
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ],
                                            label="Key Facts",
                                        ),
                                        dbc.Tab(
                                            [
                                                html.Ul(
                                                    [
                                                        html.Br(),
                                                        html.Li(
                                                            "Project title: Amazon Fine Food Reviews - Sentiment Analysis from BoW to DistilBERT Transformers"
                                                        ),
                                                        html.Li(
                                                            [
                                                                "GitHub repo: ",
                                                                html.A(
                                                                    "https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification",
                                                                    href="https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification",
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ],
                                            label="Project Info",
                                        ),
                                    ],
                                ),
                            ],
                            # style={"padding-right": "211px", "margin-top": "7px"},
                        )
                    ],
                    # width=9,
                    style={"margin-left": "20%", "margin-top": "2%"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(sidebar),
                dbc.Col(
                    width=9,
                    style={
                        "margin-left": "15px",
                        "margin-top": "7px",
                        "margin-right": "15px",
                    },
                ),
            ]
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
