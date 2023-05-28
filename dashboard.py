import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
from jupyter_dash import JupyterDash
from dash_bootstrap_templates import load_figure_template

load_figure_template("LUX")


MODELS = "Models"
MODELS = "Models"


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


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
                    # style={"width": "50%"}
                ),
                html.Br(),
                dcc.Dropdown(id="two"),
                html.Br(),
                dcc.Dropdown(id="three"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True
)
server = app.server


# Import pandas, use it to open the poverty dataset, and assign it to the variable
f_1_data = pd.read_csv("f1_data.csv")

dict_of_data = {MODELS: f_1_data}


# If we run the app now, we will get some empty figures with a white background for the
# ones where we did not set default values. For those, we also need to create empty figures,
# but set the background colors to be consistent with the whole app theme
# The dcc.Graph
# component has a figure attribute, to which we can add the empty figures with the
# desired background colors. These will be modified when users make a selection. Because
# we have a few instances of those, it's better to create a function that can be used to create
# such figures whenever we want them. The following code achieves that:
def make_empty_fig():
    fig = go.Figure()
    fig.layout.paper_bgcolor = "#E5ECF6"
    fig.layout.plot_bgcolor = "#E5ECF6"
    return fig


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
                        ),
                    ],
                    width=9,
                    style={"margin-left": "7px", "margin-top": "7px"},
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
        # html.Div(
        #     [
        #         dbc.Label("Type of research:"),
        #         dbc.Col(
        #             [
        #                 dcc.Dropdown(
        #                     id="Type_of_research",
        #                     options=[{"label": MODELS, "value": MODELS}],
        #                     placeholder="Select a type of research",
        #                     style={"width": "50%"},
        #                 ),
        #                 html.Br(),
        #                 html.Div(id="report"),
        #                 html.Br(),
        #                 # dcc.Graph(id='gini_year_barchart')
        #             ],
        #             # md=12,
        #             # lg=4,
        #         ),
        #         dcc.Loading(
        #             [
        #                 html.Div(
        #                     id="output",
        #                     children=[],
        #                     # style={"width": "50%"},
        #                 )
        #             ]
        #         ),
        #         dbc.Tabs(
        #             [
        #                 dbc.Tab(
        #                     [
        #                         html.Ul(
        #                             [
        #                                 html.Br(),
        #                                 html.Li("Number of Economies: 170"),
        #                                 html.Li("Temporal Coverage: 1974 - 2019"),
        #                                 html.Li("Update Frequency: Quarterly"),
        #                                 html.Li("Last Updated: March 18, 2020"),
        #                                 html.Li(
        #                                     [
        #                                         "Source: ",
        #                                         html.A(
        #                                             "https://datacatalog.worldbank.org/dataset/poverty-and-equity-database",
        #                                             href="https://datacatalog.worldbank.org/dataset/poverty-and-equity-database",
        #                                         ),
        #                                     ]
        #                                 ),
        #                             ]
        #                         )
        #                     ],
        #                     label="Key Facts",
        #                 ),
        #                 dbc.Tab(
        #                     [
        #                         html.Ul(
        #                             [
        #                                 html.Br(),
        #                                 html.Li(
        #                                     "Project title: Amazon Fine Food Reviews - Sentiment Analysis from BoW to DistilBERT Transformers"
        #                                 ),
        #                                 html.Li(
        #                                     [
        #                                         "GitHub repo: ",
        #                                         html.A(
        #                                             "https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification",
        #                                             href="https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification",
        #                                         ),
        #                                     ]
        #                                 ),
        #                             ]
        #                         )
        #                     ],
        #                     label="Project Info",
        #                 ),
        #             ]
        #         ),
        #     ],
        #     style={"marginLeft": 20, "marginRight": 20},
        # ),
    ],
)


@app.callback(Output("output", "children"), Input("Type_of_research", "value"))
def display_col(type_of_research):
    if type_of_research is None:
        return html.H3("")
    if type_of_research == MODELS:
        return dbc.Col(
            [
                # dbc.Label("Models:"),
                dcc.Dropdown(
                    id="Models",
                    placeholder="Select a model",
                    options=[
                        {"label": "Bag-of-words", "value": "BoW"},
                        {"label": "Word2vec", "value": "W2V"},
                        {"label": "DistilBERT", "value": "DB"},
                        {"label": "All", "value": ""},
                    ],
                    style={"width": "50%"},
                ),
                html.Br(),
                dcc.Loading([dcc.Graph(id="f1_chart", figure=make_empty_fig())]),
            ],
            # md=3,
            # lg=3,
            id="col2",
        )


@app.callback(Output("report", "children"), Input("Type_of_research", "value"))
def display_report(type_of_research):
    if type_of_research is None:
        return ""

    return [
        html.H3(type_of_research),
        f'This analysis is based on the value of f1-score-weighted for each model. The best model is DistilBERT Fine-Tuned with value of {f_1_data["f1-score-weighted"].max()}. Choose the method for text representation to see the models results.',
    ]


@app.callback(
    Output("f1_chart", "figure"),
    Input("Models", "value"),
    suppress_callback_exceptions=True,
)
def plot_f_1_data(model_type):
    fig = go.Figure()
    data_to_plot = f_1_data[f_1_data["name-method"].str.contains(str(model_type))]
    fig.add_bar(x=data_to_plot["name-method"], y=data_to_plot["f1-score-weighted"])

    if model_type == "":
        title = "F1-score-weighted for all models"
    elif model_type is not None:
        title = f"F1-score-weighted for models based on {model_type}"
    else:
        title = ""

    #     The bigger rectangle enclosing the smaller one is the "paper" area. In the charts we have
    # produced so far, it has been colored white. We can also set its color to the same color,
    # making all background colors the same for our app. We simply have to add the following
    # line to the callback functions that generate charts
    fig.layout.paper_bgcolor = "#E5ECF6"
    fig.layout.title = title
    # fig.layout.template = 'simple_white'

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
