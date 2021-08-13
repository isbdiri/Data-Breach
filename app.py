# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
import dash
import json
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_html_components as html
import visdcc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


server = app.server
app.title = "Data Breaches"

app.head = html.Link(
    rel='stylesheet',
    href='/assets/style.css'
)

#####################################################################
#################### Text to be written on page #####################
#####################################################################

heading_of_page = "Data Breaches"

explaination_text = """

                    This Dashboard aims to study the trends in Data Leaks in India 
                    over the years. 


                    1. **Victim Distribution**

                    * Analyzed how the severity of data breaches varies based on the victim count and number of data fields leaked, from a corpus of over 30 data leaks.


                    2. **Data-Breaches over Time**

                    * Aim to study the trends in Victim Count, Information lost and Frequency over the years


                    3. **Data categories and classes lost together**

                    * A visual representation of data Fields often lost together.

                    """

#####################################################################
##################### Graphs to be plotted ##########################
#####################################################################
def Network_Plot1():
    with open('./collect_data/final/network_data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    final = cyto.Cytoscape(
                            # https://dash.plotly.com/cytoscape/layout
                            id='cytoscape1',
                            elements=json_object,
                            layout={'name': 'circle'},
                            style={'width': '100%',
                                    'height': '500px',
                                    "border":"1px solid grey",
                                    "border-radius": "10px"}
                            )
    return final

def Network_Plot2():
    with open('./collect_data/final/network_clean_data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    final = visdcc.Network(data = json_object,
                    id = 'network-graph', options= dict(height= '500px', width= '95%'))
    return final

def Bar_Graph(input_val):
    group_by_year = pd.read_csv("./collect_data/final/year_bar_chart.csv")
    final = px.bar(group_by_year, x="year", y=input_val)
    return final

def Scatter_Plot():
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    fig = px.scatter(scatter_data, x="employee_count", y="exposure_index", color="category",
                 hover_data=['Org'])
    return fig

def Top_transgressors(k = 3):
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    temp = []
    for i in scatter_data['breach_count(Million)']:
        if i > 1000:
            temp.append(str(i/1000) + " B")
        elif i < 1:
            temp.append(str(i*1000) + " K")
        else:
            temp.append(str(i) + " M")
    scatter_data["breach_count_display"] = temp
    scatter_data = scatter_data[['breach_count(Million)',"breach_count_display","Org","Date"]]
    scatter_data = scatter_data.sort_values(by=['breach_count(Million)'], ascending=False)
    output = [html.H3("Top " + str(k) + " transgressors", className="sub-sub-head"), dbc.Row([dbc.Col("Organisation"), dbc.Col("Number of victims"), dbc.Col("Date")], className="data-table-row")]
    temp = [dbc.Col( [ html.P(i) for i in list(scatter_data["Org"].head(k))] )]
    temp.append(dbc.Col( [ html.P(i) for i in list(scatter_data["breach_count_display"].head(k))] ))
    temp.append(dbc.Col( [ html.P(i) for i in list(scatter_data["Date"].head(k))] ))
    output.append(dbc.Row(temp))
    output = dbc.Col(output)
    return output

def Overview_of_scatter():
    final_out = []
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")

    # categories
    temp = [ html.H5("Category of organizations") ]
    temp.append(html.P(str(len(scatter_data["category"].unique()))))
    final_out.append( dbc.Col(temp, className="scatter-overview") )
    
    # Count Victims
    temp = [ html.H5("Victims of breach")]
    count = sum(scatter_data["breach_count(Million)"])
    if count > 1000:
        count = str(int(count/1000)) + " B+"
    elif count < 1:
        count = str(int(count*1000)) + " K+"
    else:
        count = str(int(count)) + " M+"
    temp.append(html.P(count))
    final_out.append( dbc.Col(temp, className="scatter-overview") )

    # orgs reviewed
    temp = [ html.H5("Organizations reviewed") ]
    temp.append(html.P(str(len(scatter_data["Org"].unique()))))
    final_out.append( dbc.Col(temp, className="scatter-overview") )

    final_out = dbc.Row(final_out)
    return final_out

#####################################################################
######################## Callback Functions #########################
#####################################################################

@app.callback(Output('container-button-timestamp', 'children'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks'))
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        return dcc.Graph(figure=Bar_Graph("count"))
    elif 'btn-nclicks-2' in changed_id:
        return dcc.Graph(figure=Bar_Graph("sum"))
    elif 'btn-nclicks-3' in changed_id:
        return dcc.Graph(figure=Bar_Graph("info_lost"))
    else:
        return dcc.Graph(figure=Bar_Graph("count"))

@app.callback(Output('container-trangressor-count', 'children'),
                Input('num-multi', 'value'))
def changeCount(x):
    return Top_transgressors(x)
#####################################################################
############################ App Layout #############################
#####################################################################
app.layout = html.Div([dbc.Row([
            dbc.Col([
                    dbc.Row([
                            html.H1(html.P(heading_of_page, className="top-head")),
                            html.Div(dcc.Markdown(explaination_text), className="top-desc")
                            ]),
                    ], width=3, style={"position":"fixed"},className="left-col"),
            dbc.Col([ 
                    dbc.Row(html.H2("Victim Distribution"), className="sub-head"),
                    dbc.Row([
                            dbc.Col([
                                    html.P("Select top"),
                                    dcc.Input(
                                            id='num-multi',
                                            type='number',
                                            value=3,
                                            min = 1,
                                            max = 10,
                                            className="inpt"
                                            ),
                                    html.P("Victims"),
                                    html.Div(id='container-trangressor-count')
                                    ], width=5),
                            dbc.Col([
                                    Overview_of_scatter(),
                                    dcc.Graph(figure=Scatter_Plot())
                                    ], width=7)
                            ]),
                    dbc.Row(html.H2("Intensity of Data-Breaches over Time: "), className="sub-head"),
                    dbc.Row([
                            dbc.Col([
                                        dbc.Row(dbc.Button('Breach count', id='btn-nclicks-1', n_clicks=0,outline=True, color="info", size="lg"),align="start"),
                                        dbc.Row(dbc.Button('Individuals impacted', id='btn-nclicks-2', n_clicks=0,outline=True, color="info", size="lg"),align="center"),
                                        dbc.Row(dbc.Button('Information lost', id='btn-nclicks-3', n_clicks=0,outline=True, color="info", size="lg"),align="end"),
                                    ], width=3, style={"padding-top": "3%", "justify-content":"space-between", "display":"flex", "flex-direction":"column", "padding-top":"6%", "padding-bottom":"9%"}),
                            dbc.Col(html.Div(id='container-button-timestamp'),width=9),
                            ]),
                    dbc.Row(html.H2("Data categories and classes generally lost together: "), className="sub-head"),
                    dbc.Row([
                            dbc.Col(Network_Plot1(),width=4),
                            dbc.Col(Network_Plot2(),width=8, style={"border":"1px solid grey","border-radius": "10px", "margin": '0px', "padding": "0px"}),
                            ]),
                    ], 
            width="auto", style={"padding-top": "3%", "padding-left": "27%","padding-bottom": "3%"})
    ],)],
    style={
                "padding": "0%"
            }
)

app.run_server(debug=True)