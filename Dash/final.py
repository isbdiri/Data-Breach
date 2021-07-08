# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
import dash
import json
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])

#####################################################################
#################### Text to be written on page #####################
#####################################################################

heading_of_page = "HHHHHEEEEAAADDDIIINNNGGG"

explaination_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisi odio, iaculis at aliquam quis, sagittis quis quam. Vestibulum malesuada, leo vel maximus dignissim, justo felis dictum purus, eget convallis massa metus at purus. Vestibulum elementum leo vitae risus hendrerit pharetra. Proin magna nisi, maximus in quam sit amet, malesuada sollicitudin massa. Maecenas malesuada enim vel nulla congue euismod. Nulla facilisi. Pellentesque sit amet convallis nisl, sit amet interdum tortor. Cras a nulla consequat, scelerisque felis vitae, gravida quam. Phasellus varius, ipsum eu luctus pulvinar, est lectus luctus nunc, eu efficitur lectus massa et erat.


Proin eget venenatis nisi. Integer mollis ornare quam, ac finibus justo malesuada quis. Nam efficitur ut mauris sit amet tempus. Donec vel purus mauris. Aliquam et orci non lorem tincidunt elementum. Nullam sollicitudin egestas nisl ut fermentum. Duis auctor risus sit amet diam vulputate, tincidunt bibendum quam suscipit."""

#####################################################################
##################### Graphs to be plotted ##########################
#####################################################################
def Network_Plot():
    with open('../collect_data/final/network_data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    final = cyto.Cytoscape(
                            # https://dash.plotly.com/cytoscape/layout
                            id='cytoscape',
                            elements=json_object,
                            layout={'name': 'circle'},
                            style={'width': '100%', 'height': '800px'}
                            )
    return final

def Bar_Graph():
    group_by_year = pd.read_csv("../collect_data/final/year_bar_chart.csv")
    final = px.bar(group_by_year, x="year", y="Date")
    return final

def Scatter_Plot():
    scatter_data = pd.read_csv("../collect_data/final/scatter_data.csv")
    fig = px.scatter(scatter_data, x="employee_count", y="exposure_index", color="category",
                 hover_data=['Org'])
    return fig

#####################################################################
############################ App Layout #############################
#####################################################################
app.layout = html.Div(
    [
        html.H1(heading_of_page),
        dbc.Row(
            [
                dbc.Col([
                        html.Div(dcc.Markdown(explaination_text)),
                        Network_Plot()
                        ], width=8),
                # dbc.Col(html.Div("One of three columns"), width=3),
                dbc.Col([
                            dcc.Graph(figure=Scatter_Plot()),
                            dcc.Graph(figure=Bar_Graph()),
                        ], width=4), 
            ],
        ),
    ]
)

app.run_server(debug=True)