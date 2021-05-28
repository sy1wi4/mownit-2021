# Run this app with `python lorenz_attractor.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from numpy import array, linspace
from scipy.integrate import solve_ivp


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#1C0F4B',
    'text': '#7FDBFF'
}


# parameters
a = 10
c = 28
b = 2


def f(t, r):
    x, y, z = r
    fx = a * (y - x)
    fy = c * x - y - x * z
    fz = x * y - b * z
    return array([fx, fy, fz], float)


# y0 - initial values
# interval - interval of integration
# points - number if points

def solve(y0, interval, points):
    interval_from, interval_to = interval

    solution = solve_ivp(f, [interval_from, interval_to], y0, t_eval=linspace(interval_from, interval_to, points))

    return solution


y0 = [0, 1, 0]
interval = [0, 50]
points = 5000

sol = solve(y0, interval, points)


def set_fig(sol):
    fig = go.Figure(data=[go.Scatter3d(x=sol.y[0, :], y=sol.y[1, :], z=sol.y[2, :],
                                       marker=dict(
                                           size=0.01,
                                           color=sol.y[2, :],
                                       ),
                                       line=dict(
                                           color=sol.y[2, :],
                                           width=3
                                       ))])

    fig.update_layout(
        autosize=False,
        width=1000,
        height=700,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='LORENZ ATTRACTOR',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Lorenz Attractor equations solver using Runge-Kutta method', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='graph',
            figure=fig
        ),

        html.Div(id='selected-a', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        html.Div(id='selected-b', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        html.Div(id='selected-c', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Slider(id='a',
                   min=0,
                   max=20,
                   step=0.5,
                   value=a,
                   marks={i: str(i) for i in range(0, 21)}
                   ),

        dcc.Slider(id='b',
                   min=0,
                   max=20,
                   step=0.5,
                   value=b,
                   marks={i: str(i) for i in range(0, 21)}
                   ),

        dcc.Slider(id='c',
                   min=0,
                   max=20,
                   step=0.5,
                   value=c,
                   marks={i: str(i) for i in range(0, 21)}
                   ),

    ])

    return fig


@app.callback(Output(component_id='graph', component_property='figure'),
              Input('a', 'value'), Input('b', 'value'), Input('c', 'value'))
def update_param(new_a, new_b, new_c):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    global sol

    if trigger_id == 'a':
        global a, sol
        a = new_a
    elif trigger_id == 'b':
        global b, sol
        b = new_b
    elif trigger_id == 'c':
        global c, sol
        c = new_c

    sol = solve(y0, interval, points)
    fig = set_fig(sol)

    return fig


@app.callback(Output(component_id='selected-a', component_property='children'), Input('a', 'value'))
def show_param(new_a):
    return 'a: {}'.format(new_a)


@app.callback(Output(component_id='selected-b', component_property='children'), Input('b', 'value'))
def show_param(new_b):
    return 'b: {}'.format(new_b)


@app.callback(Output(component_id='selected-c', component_property='children'), Input('c', 'value'))
def show_param(new_c):
    return 'c: {}'.format(new_c)


if __name__ == '__main__':
    set_fig(sol)
    app.run_server(debug=True)
