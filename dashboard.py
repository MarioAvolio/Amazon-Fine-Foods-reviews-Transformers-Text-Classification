import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd

MODELS="Models"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])


# Import pandas, use it to open the poverty dataset, and assign it to the variable
f_1_data = pd.read_csv('f1_data.csv')

dict_of_data = {
    MODELS: f_1_data
}

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
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = '#E5ECF6'
    return fig



app.layout = html.Div([
    html.H1('Amazon Fine Food Reviews', style={'textAlign': 'center'}),
    html.H2('Sentiment Analysis from BoW to DistilBERT Transformers', style={'textAlign': 'center'}),
    html.H3('Choose the type of research:', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Label("Type of research:"),
        dbc.Col([
            dcc.Dropdown(id='Type_of_research',
                options=[{'label': MODELS , 'value': MODELS}], 
                placeholder="Select a type of research",),
            html.Br(),
            html.Div(id='report'),
            html.Br(), 
            
            # dcc.Graph(id='gini_year_barchart')
        ]),
        
        dbc.Col([
            # dbc.Label("Models:"),
            dcc.Dropdown(id='Models',
                         placeholder="Select a model",
                        options=[{'label': "Bag-of-words", 'value': "BoW"},
                                {'label': "Word2vec", 'value': "W2V"}, 
                                {'label': "DistilBERT", 'value': "DB"}, {'label': "All", 'value': ""}]),
            html.Br(),
            dcc.Graph(id='f1_chart', figure=make_empty_fig()),
    
        ], md=12, lg=8), # Another thing we need to handle is how the resizing of the browser window affects the
# size and placement of our different components. The figures are responsive by default, but
# we need to make some decisions for the figures that are placed side by side
        
    ]),
   
    
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
                html.Li('Project title: Amazon Fine Food Reviews - Sentiment Analysis from BoW to DistilBERT Transformers'),
                html.Li(['GitHub repo: ',
                         html.A('https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification',
                                href='https://github.com/MarioAvolio/Amazon-Fine-Foods-reviews-Transformers-Text-Classification')
                         ])
            ])
        ], label='Project Info')
    ]),

    
], style={'backgroundColor': '#E5ECF6'}) # Another thing we can consider doing is making our theme consistent with the theme
# of the charts that we are using. We can set the background color of the app to the same
# default color used in Plotly's figures. 


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
    
    if model_type == '':
        title = 'F1-score-weighted for all models'
    elif model_type is not None:
        title = f'F1-score-weighted for models based on {model_type}'
    else:
        title=''
    
#     The bigger rectangle enclosing the smaller one is the "paper" area. In the charts we have
# produced so far, it has been colored white. We can also set its color to the same color,
# making all background colors the same for our app. We simply have to add the following
# line to the callback functions that generate charts
    fig.layout.paper_bgcolor = '#E5ECF6' 
    fig.layout.title = title
    # fig.layout.template = 'simple_white'

    return fig






if __name__ == '__main__':
    app.run_server(debug=True)
