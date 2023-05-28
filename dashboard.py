import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd
MODELS="Models"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Import pandas, use it to open the poverty dataset, and assign it to the variable
f_1_data = pd.read_csv('f1_data.csv')

dict_of_data = {
    MODELS: f_1_data
}


app.layout = html.Div([
    html.H1('Amazon Fine Food Reviews'),
    html.H2('Sentiment Analysis from BoW to DistilBERT Transformers'),
    html.H3('Choose the type of research:'),

    dcc.Dropdown(id='Type_of_research',
                options=[{'label': MODELS , 'value': MODELS}]),
    
    html.Br(),
    html.Div(id='report'),
    html.Br(),
    
    dcc.Dropdown(id='Models',
                options=[{'label': "Bag-of-words", 'value': "BoW"},
                         {'label': "Word2vec", 'value': "W2V"}, 
                         {'label': "DistilBERT", 'value': "DB"}, {'label': "All", 'value': ""}]),
    dcc.Graph(id='f1_chart'),
    
    
    dbc.Tabs([
       dbc.Tab([
           html.Ul([
               html.Br(),
               html.Li('Number of Economies: 170'),
               html.Li('Temporal Coverage: 1974 - 2019'),
               html.Li('Update Frequency: Quarterly'),
               html.Li('Last Updated: March 18, 2020'),
               html.Li([
                   'Source: ',
                   html.A('https://datacatalog.worldbank.org/dataset/poverty-and-equity-database',
                          href='https://datacatalog.worldbank.org/dataset/poverty-and-equity-database')
               ])
           ])

       ], label='Key Facts'),
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('Book title: Interactive Dashboards and Data Apps with Plotly and Dash'),
                html.Li(['GitHub repo: ',
                         html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash',
                                href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')
                         ])
            ])
        ], label='Project Info')
    ]),

    
])


@app.callback(Output('report', 'children'),
              Input('Type_of_research', 'value'))
def display_report(type_of_research):
    if type_of_research is None:
        return ''

    return [html.H3(type_of_research),
            f'This analysis is based on the value of f1-score-weighted for each model. The best model is DistilBERT Fine-Tuned with value of {f_1_data["f1-score-weighted"].max()}. Choose the method for text representation to see the models results.']



@app.callback(Output('f1_chart', 'figure'), Input('Models', 'value'))
def plot_f_1_data(model_type):
    fig = go.Figure()
    data_to_plot = f_1_data[f_1_data['name-method'].str.contains(str(model_type))]
    fig.add_bar(x=data_to_plot['name-method'],
                y=data_to_plot['f1-score-weighted'])
    fig.layout.title = 'Summary Models'
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
