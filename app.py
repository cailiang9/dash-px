from subprocess import os
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

tips = px.data.tips()
col_options = [dict(label=x, value=x) for x in tips.columns]
dimensions = [ "x", "y", "color", "facet_col", "facet_row"]

prefix='/dash/'
port=int(os.environ.get("PORT", 22078))
import requests
res = requests.post('http://127.0.0.1:8082/api/routes/'+prefix, data='''{"target": "http://127.0.0.1:%d"}'''%port)
print(res.status_code)
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"], routes_pathname_prefix=prefix
)

GRAPH_INTERVAL = int(os.environ.get("GRAPH_INTERVAL", 5000))
app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
        html.Div(
            [
                html.Div([d + ":", dcc.Dropdown(id=d, value=value, options=col_options)])
                for d,value in zip(dimensions, 'total_bill tip size sex day'.split())
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
        dcc.Interval(
            id="update-interval",
            interval=int(GRAPH_INTERVAL),
            n_intervals=0,
        ),
    ]
)


@app.callback(Output("graph", "figure"), [Input("update-interval", "n_intervals")]+[Input(d, "value") for d in dimensions])
def make_figure(update_interval, x, y, color, facet_col, facet_row):
    return px.scatter(
        tips,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        color_continuous_scale=px.colors.diverging.Spectral[::-1],
        title=str(update_interval)
    )

app.run_server(debug=True, port=port)
