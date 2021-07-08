import dash,json
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])


with open('../collect_data/final/network_data.json', 'r') as openfile:
  
    # Reading from json file
    json_object = json.load(openfile)
    print(json_object)

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        # https://dash.plotly.com/cytoscape/layout
        id='cytoscape',
        # elements=[
        #     {'data': {'id': 'ca', 'label': 'Canada'}}, 
        #     {'data': {'id': 'on', 'label': 'Ontario'}}, 
        #     {'data': {'id': 'qc', 'label': 'Quebec'}},
        #     {'data': {'source': 'ca', 'target': 'on'}}, 
        #     {'data': {'source': 'ca', 'target': 'qc'}}
        # ],
        elements=json_object,
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '500px'}
    )
])

app.run_server(debug=True)