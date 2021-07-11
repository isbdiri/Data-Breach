# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
import dash
import json
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output
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
def Network_Plot1():
    with open('../collect_data/final/network_data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    final = cyto.Cytoscape(
                            # https://dash.plotly.com/cytoscape/layout
                            id='cytoscape1',
                            elements=json_object,
                            layout={'name': 'circle'},
                            style={'width': '80%', 'height': '500px'}
                            )
    return final

def Network_Plot2():
    with open('../collect_data/final/network_clean_data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    final = cyto.Cytoscape(
                            # https://dash.plotly.com/cytoscape/layout
                            id='cytoscape2',
                            elements=json_object,
                            layout={'name': 'breadthfirst'},
                            style={'width': '80%', 'height': '500px'}
                            )
    return final

def Bar_Graph(input_val):
    group_by_year = pd.read_csv("../collect_data/final/year_bar_chart.csv")
    final = px.bar(group_by_year, x="year", y=input_val)
    return final

def Scatter_Plot():
    scatter_data = pd.read_csv("../collect_data/final/scatter_data.csv")
    fig = px.scatter(scatter_data, x="employee_count", y="exposure_index", color="category",
                 hover_data=['Org'])
    return fig

def Top_transgressors(k = 3):
    scatter_data = pd.read_csv("../collect_data/final/scatter_data.csv")
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
    output = [html.H3("Top " + str(k) + " transgressors")]
    temp = [dbc.Col( [ html.P(i) for i in list(scatter_data["Org"].head(k))] )]
    temp.append(dbc.Col( [ html.P(i) for i in list(scatter_data["breach_count_display"].head(k))] ))
    temp.append(dbc.Col( [ html.P(i) for i in list(scatter_data["Date"].head(k))] ))
    output.append(dbc.Row(temp))
    output = dbc.Col(output)
    return output

def Overview_of_scatter():
    final_out = []
    scatter_data = pd.read_csv("../collect_data/final/scatter_data.csv")

    # categories
    temp = [ html.H4("Category of organizations") ]
    temp.append(html.P(str(len(scatter_data["category"].unique()))))
    final_out.append( dbc.Col(temp) )
    
    # Count Victims
    temp = [ html.H4("Victims of breach") ]
    count = sum(scatter_data["breach_count(Million)"])
    if count > 1000:
        count = str(int(count/1000)) + " B+"
    elif count < 1:
        count = str(int(count*1000)) + " K+"
    else:
        count = str(int(count)) + " M+"
    temp.append(html.P(count))
    final_out.append( dbc.Col(temp) )

    # orgs reviewed
    temp = [ html.H4("Organizations reviewed") ]
    temp.append(html.P(str(len(scatter_data["Org"].unique()))))
    final_out.append( dbc.Col(temp) )

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
                        Network_Plot1(),
                        Network_Plot2()
                        ], width=5),
                dbc.Col([
                        dbc.Row([
                                dbc.Col(Top_transgressors(3), width=4),
                                dbc.Col([
                                        Overview_of_scatter(),
                                        dcc.Graph(figure=Scatter_Plot())
                                        ])
                                ]),
                        dbc.Row([
                            dbc.Col(html.Button('Breach count', id='btn-nclicks-1', n_clicks=0)),
                            dbc.Col(html.Button('Individuals impacted', id='btn-nclicks-2', n_clicks=0)),
                            dbc.Col(html.Button('Information lost', id='btn-nclicks-3', n_clicks=0)),
                        ]),
                        html.Div(id='container-button-timestamp'),
                        # dcc.Graph(figure=Bar_Graph("count")),
                        ], width=7), 
            ],
        ),
    ],
    style={
                "padding": "2%"
            }
)

app.run_server(debug=True)