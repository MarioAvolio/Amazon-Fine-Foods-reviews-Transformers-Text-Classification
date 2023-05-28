import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Import pandas, use it to open the poverty dataset, and assign it to the variable
f_1_data = pd.read_csv('f1_data.csv')
print(f_1_data)


app.layout = html.Div([
    html.H1('Amazon Fine Food Reviews'),
    html.H2('Sentiment Analysis from BoW to DistilBERT Transformerk'),
    dcc.Dropdown(id='Models',
                options=[{'label': "Bag-of-words", 'value': "BoW"}, {'label': "Word2vec", 'value': "W2V"}, {'label': "DistilBERT", 'value': "DB"}, {'label': "All", 'value': ""}]),
    dcc.Graph(id='population_chart'),
    
])


@app.callback(Output('population_chart', 'figure'), Input('Models', 'value'))
def plot_f_1_data(model_type):
    fig = go.Figure()
    data_to_plot = f_1_data[f_1_data['name-method'].str.contains(str(model_type))]
    fig.add_bar(x=data_to_plot['name-method'],
                y=data_to_plot['f1-score-weighted'])
    fig.layout.title = 'Summary Models'
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
