import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

from constants import MODELS, SIDEBAR_STYLE, WORD_COUNTS
import os

load_figure_template("LUX")

# ----------------------- VARIABLE -----------------------

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True
)


# to get the current working directory
directory = os.getcwd()
subdir = os.path.join(directory, "mydash")

dict_most_common = {
    "from_mislabeled_classes": "Most common words with not ascending loss",
    "from_confident_classes": "Most common words with ascending loss",
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
                    options=[
                        {"label": MODELS, "value": MODELS},
                        {"label": WORD_COUNTS, "value": WORD_COUNTS},
                    ],
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
common_words_df = pd.read_csv(os.path.join(subdir, "common_words_df.csv"))


dict_of_data = {MODELS: f_1_data, WORD_COUNTS: common_words_df}

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
    if type_of_research == WORD_COUNTS:
        return [
            {"label": "Confident predictions", "value": "from_confident_classes"},
            {"label": "Mislabeled predictions", "value": "from_mislabeled_classes"},
            {"label": "All", "value": "all"},
        ]


def get_f1_plot(filter, fig):
    data_to_plot = f_1_data[f_1_data["name-method"].str.contains(str(filter))]
    fig.add_bar(x=data_to_plot["name-method"], y=data_to_plot["f1-score-weighted"])

    if filter == "":
        title = "F1-score-weighted for all models"
    elif filter is not None:
        title = f"F1-score-weighted for models based on {filter}"
    else:
        title = ""

    fig.update_layout(
        title={
            "text": title,
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        yaxis_title="F1-score weighted",
        xaxis_title="Models type",
        # legend_title="Legend Title",
        font=dict(
            # family="Courier New, monospace",
            size=14,
            # color="RebeccaPurple"
        ),
    )
    return fig


def get_common_words_plot(filter, fig):
    if str(filter) == "all":
        words = common_words_df.word.tolist()

        number_from_mislabeled_classes = common_words_df.from_mislabeled_classes.tolist()
        number_from_confident_classes = common_words_df.from_confident_classes.tolist()
        title = "Most common words from mislabeled and confident predictions"
        fig.add_trace(
            go.Bar(
                x=words,
                y=number_from_mislabeled_classes,
                name="From Mislabeled Prediction",
                marker_color="rgb(55, 83, 109)",
            )
        )
        fig.add_trace(
            go.Bar(
                x=words,
                y=number_from_confident_classes,
                name="From Confident Prediction",
                marker_color="rgb(26, 118, 255)",
            )
        )

        fig.update_layout(
            legend=dict(
                x=0,
                y=1.0,
                bgcolor="rgba(255, 255, 255, 0)",
                bordercolor="rgba(255, 255, 255, 0)",
            ),
            barmode="group",
            bargap=0.5,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.25,  # gap between bars of the same location coordinate.
        )
    else:
        words = common_words_df[common_words_df[filter] != 0].word.tolist()
        # print(words)
        number = common_words_df[common_words_df[filter] != 0][str(filter)].to_list()
        fig.add_bar(x=words, y=number)

        title = dict_most_common[filter]

    fig.update_layout(
        title={"text": title}, yaxis_title="Number of occurences", xaxis_title="Words"
    )

    # print(fig)
    return fig


@app.callback(
    Output("output", "figure"),
    Input("filter", "value"),
    Input("Type_of_research", "value"),
)
def plot_data(filter, type_of_research):
    fig = go.Figure()

    if str(type_of_research) == MODELS:
        fig = get_f1_plot(filter, fig)
    elif str(type_of_research) == WORD_COUNTS:
        fig = get_common_words_plot(filter, fig)

    # print(fig)
    fig.layout.template = "simple_white"
    fig.update_layout(
        title={
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            titlefont_size=16,
            tickfont_size=14,
        ),
        font=dict(
            size=14,
        ),
    )
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
                            "Sentiment Analysis from BoW to DistilBERT Transformer",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    [
                                        dcc.Graph(
                                            id="output",
                                            style={"width": "100%", "height": "700px"},
                                        )
                                    ]
                                ),
                            ],
                            style={"margin-top": "5%", "margin-left": "-50px"},
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
                                                            "Project title: Amazon Fine Food Reviews - Sentiment Analysis from BoW to DistilBERT Transformer"
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
