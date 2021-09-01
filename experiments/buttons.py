import dash
import dash_html_components as html
from dash.dependencies import Output, Input
from dash import callback_context

n_buttons = 5
# Create example app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([html.Button("Button {}".format(i), id=str(i)) for i in range(n_buttons)] + [html.Div(id="log")])


@app.callback(Output("log", "children"), [Input(str(i), "n_clicks") for i in range(n_buttons)])
def func(*args):
    trigger = callback_context.triggered[0] 
    return "You clicked button {}".format(trigger["prop_id"].split(".")[0])


if __name__ == '__main__':
    app.run_server()