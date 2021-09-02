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

                    * Studied the trends in Victim Count, Information lost and Frequency over the years.

                    3. **Across Organizations Category**

                    * A visual representation of impact of leaks across different organization Categories.


                    4. **Data categories and classes lost together**

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

def custom_bubbles(input_str):
    input_str = "".join(input_str.split("'"))
    input_str = "".join(input_str.split("\""))
    input_str = input_str.split(",")
    temp = []
    for i in input_str:
        temp1 = i.split(" ")
        while 1:
            try:
                temp1.remove('')
            except:
                break
        temp.append(" ".join(temp1))
    input_str = temp
    # print(type(input_str))
    # print(input_str)
    plot_data = {"nodes":[], "edges":[]}
    for i in input_str:
        plot_data["nodes"].append(
            {"id": i,
            "label": i})
        if i != input_str[0]:
            plot_data["edges"].append(
                {
                "id": input_str[0] + "_to_" + i ,
                "from": input_str[0],
                "to": i
                })
    return_val = visdcc.Network(data = plot_data,
                    id = 'Bubble-graph', options= dict(height= '500px', width= '95%'))
    return return_val

def Bar_Graph(input_val):
    group_by_year = pd.read_csv("./collect_data/final/year_bar_chart.csv")
    final = px.bar(group_by_year, x="year", y=input_val)
    return final

def Scatter_Plot():
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    fig = px.scatter(scatter_data, x="employee_count", y="Relative Exposure Index", color="category",
                 hover_data=['Org'])
    return fig

def Top_transgressors(k = 3):
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    scatter_data["Date"] = pd.to_datetime(scatter_data["Date"])
    temp = []
    for i in scatter_data['breach_count(Million)']:
        if i > 1000:
            temp.append(str(int(i)) + " M")
        elif i < 1:
            temp.append(str(int(i*1000)) + " K")
        else:
            temp.append(str(int(i)) + " M")
    scatter_data["breach_count_display"] = temp
    scatter_data = scatter_data[['breach_count(Million)',"breach_count_display","Org","Date"]]
    scatter_data = scatter_data.sort_values(by=['breach_count(Million)'], ascending=False)
    # output = [html.H3("Top " + str(k) + " transgressors", className="sub-sub-head"), dbc.Row([dbc.Col("Organisation"), dbc.Col("Number of victims"), dbc.Col("Date")], className="data-table-row")]
    output = [ dbc.Row([dbc.Col("Organisation"), dbc.Col("Number of victims"), dbc.Col("Date")], className="data-table-row")]
    temp = [dbc.Col( [ dbc.Button(i, style={"padding-right":"100px"}, color="light",id=str("trangressors_" + str(num)) ) for num,i in enumerate(list(scatter_data["Org"].head(k)))])]
    # temp,  Buttons_callback_input = [], [Input('default', 'n_clicks')]
    # for num, i in enumerate(list(scatter_data["Org"].head(k))):
        # temp.append(dbc.Button(i, style={"padding-right":"100px"},id=str("trangressors_" + str(num)), color="light", n_clicks=0))
        # temp.append(html.Button(i,id=str("trangressors_" + str(num))))
        # Buttons_callback_input.append(Input(str("trangressors_" + str(num)), "n_clicks"))
    
    temp = [dbc.Col(temp)]
    temp.append(dbc.Col( [ html.P(i) for i in list(scatter_data["breach_count_display"].head(k))] ))
    temp.append(dbc.Col( [ html.P(str(i.month) + "-" + str(i.year)) for i in list(scatter_data["Date"].head(k))] ))
    output.append(dbc.Row(temp))
    output = dbc.Col(output)
    return output

def Overview_of_scatter():
    final_out = []
    scatter_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    
    # orgs reviewed
    temp = [ html.H5("Companies") ]
    temp.append(html.P(str(len(scatter_data["Org"].unique()))))
    final_out.append( dbc.Col(temp, className="scatter-overview") )


    # categories
    temp = [ html.H5("Categories") ]
    temp.append(html.P(str(len(scatter_data["category"].unique()))))
    final_out.append( dbc.Col(temp, className="scatter-overview") )
    
    # Count Victims
    temp = [ html.H5("Victims")]
    count = sum(scatter_data["breach_count(Million)"])
    if count > 1000:
        count = str(int(count/1000)) + " B+"
    elif count < 1:
        count = str(int(count*1000)) + " K+"
    else:
        count = str(int(count)) + " M+"
    temp.append(html.P(count))
    final_out.append( dbc.Col(temp, className="scatter-overview") )

    final_out = dbc.Row(final_out)
    return final_out

def Pie_chart():
    df = pd.read_csv("./collect_data/final/Org_cats.csv")
    fig = px.pie(df, values='Victim Count (Million)', names='category')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig

def Bubble_chart_orgcat():
    df = pd.read_csv("./collect_data/final/Org_cats.csv")
    fig = px.scatter(df, x="category", y="Victim Count (Million)", color="category",
                     size="Bubble Size", text="Number of Breaches")
    return fig

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
        return dcc.Graph(figure=Bar_Graph("Number of Data Breaches"))
    elif 'btn-nclicks-2' in changed_id:
        return dcc.Graph(figure=Bar_Graph("Individuals impacted (Millions)"))
    elif 'btn-nclicks-3' in changed_id:
        return dcc.Graph(figure=Bar_Graph("Cumulative Exposure Index"))
    else:
        return dcc.Graph(figure=Bar_Graph("Number of Data Breaches"))


@app.callback(Output('change_scatter_with_bubble', 'children'),
                [Input('default', 'n_clicks')] + [Input('trangressors_' + str(i), 'n_clicks') for i in range(15)])
def changeCount(*buttons_input):
    Df_bubble_data = pd.read_csv("./collect_data/final/scatter_data.csv")
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    trigger = dash.callback_context.triggered[0] 
    trigger = trigger["prop_id"].split(".")[0]
    final = [Overview_of_scatter(),
            dcc.Graph(figure=Scatter_Plot())
            ]
    if trigger == "default":
        return final
    try:
        trigger = trigger.split("_")[-1]
        trigger = int(trigger)
        final = custom_bubbles(Df_bubble_data["data_classes"][trigger][1:-1])
        # final = [html.H2("Data Fields Leaked:")].append(dcc.Graph(figure=final))
        return final
    except ValueError:
        return final

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
                    dbc.Row(html.H2("Victim Distribution: "), className="sub-head"),
                    dbc.Row([
                            dbc.Col([
                                    dbc.Row([html.H3("Top 15 transgressors:", className="sub-sub-head"),
                                                dbc.Button("Reset", id='default',color="dark",outline=True, n_clicks=0, style={"align":"right"})
                                            ]),
                                    # html.P("Select top"),
                                    # dcc.Input(
                                    #         id='num-multi',
                                    #         type='number',
                                    #         value=6,
                                    #         min = 1,
                                    #         max = 10,
                                    #         className="inpt"
                                    #         ),
                                    # html.P("Victims"),
                                    # html.Div(id='container-trangressor-count')
                                    html.Div(Top_transgressors(15)),
                                    ], width=5),
                            # dbc.Col([
                            #         Overview_of_scatter(),
                            #         dcc.Graph(figure=Scatter_Plot())
                            #         ], width=7)
                            dbc.Col(
                                html.Div(id="change_scatter_with_bubble"),
                                width=7)
                            ]),
                    dbc.Row(html.H2("Intensity of Data-Breaches over Time: "), className="sub-head"),
                    dbc.Row([
                            dbc.Col([
                                        dbc.Row(dbc.Button('Breach count', id='btn-nclicks-1', n_clicks=0,outline=True, color="info", size="lg"),align="start"),
                                        dbc.Row(dbc.Button('Individuals impacted', id='btn-nclicks-2', n_clicks=0,outline=True, color="info", size="lg"),align="center"),
                                        dbc.Row(dbc.Button('Exposure Index', id='btn-nclicks-3', n_clicks=0,outline=True, color="info", size="lg"),align="end"),
                                    ], width=3, style={"padding-top": "3%", "justify-content":"space-between", "display":"flex", "flex-direction":"column", "padding-top":"6%", "padding-bottom":"9%"}),
                            dbc.Col(html.Div(id='container-button-timestamp'),width=9),
                            ]),
                    dbc.Row(html.H2("Analysis across Organizations Category: "), className="sub-head"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=Bubble_chart_orgcat(), id="orgcat_bubbleplot"), style={"border":"1px solid grey","border-radius": "10px", "padding": "0px", "margin": '0px'},width=7),
                        dbc.Col(dcc.Graph(figure=Pie_chart()), style={"border":"1px solid grey","border-radius": "10px", "padding": "0px", "margin": '0px'},width=5),
                        ]),
                    dbc.Row(html.H2("Data categories and classes generally lost together: "), className="sub-head"),
                    dbc.Row([
                            dbc.Col(Network_Plot1(),width=4),
                            dbc.Col(Network_Plot2(),width=8, style={"border":"1px solid grey","border-radius": "10px", "margin": '0px', "padding": "0px"}),
                            ]),
                    html.Div(id="test"),
                    ], 
            width="auto", style={"padding-top": "1%", "padding-left": "26.5%","padding-bottom": "3%"})
    ],)],
    style={
                "padding": "0%"
            }
)

if __name__ == '__main__':
    app.run_server(debug=True)