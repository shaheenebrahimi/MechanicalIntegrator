# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# import numpy as np
# 
# from dash.dependencies import Input, Output

import plotly.io as pio

fig = dict({
    'data': [
        {'type': 'scatter',
         'x': [],
         'y': [],
         }],
    'layout': {
        'title': {
            'text': 'Chart'
            }
        }
    })

pio.show(fig)

def sumthn():
    for i in range(10):
        x = []
        y = []
        x.append(i)
        y.append(i)
        fig['data'] = [
            {'type': 'scatter',
             'x': x,
             'y': y,
             }]

sumthn()



# Example data (a circle).
# resolution = 100
# t = np.linspace(0, np.pi * 2, resolution)
# x, y = np.cos(t), np.sin(t)
# # Example app.
# figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-1, 1]), yaxis=dict(range=[-1, 1])))
# app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
# app.layout = html.Div([dcc.Graph(id='graph', figure=figure), dcc.Interval(id="interval", interval=5000)])
# 
# 
# @app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
# def update_data(n_intervals):
#     print("Intervals: ", n_intervals, " Index: ", n_intervals % resolution)
#     index = n_intervals % resolution
#     # tuple is (dict of new data, target trace index, number of points to keep)
#     return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
# 
# def setValues(xVals, yVals):
#     x = xVals
#     y = yVals
#     
# def createGraph():
#     app.run_server()
# 
# createGraph()


# import dash
# import plotly
# from dash import html
# from dash import dcc
# import numpy as np
# 
# from dash.dependencies import Input, Output
# 
# x = [0]
# y = [0]
#     
# app = dash.Dash(__name__)
# app.layout = html.Div([
#     dcc.Graph(id='live-graph', animate=True),
#     dcc.Interval(id='graph-update', interval=25, n_intervals=0),
# ])
# 
# @app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
# def update_graph(n):
#     x.append(x[-1]+1)
#     y.append(y[-1]+2)
#     data = plotly.graph_objs.Scatter(x=list(x), y=list(y), name='Input Function', mode='lines+markers')
#     return {'data': [data], 'layout': goLayout(xaxis=dict(range=[-2,2]), yaxis=dict(range=[-4,4]), )}
# 
#     
# # def createGraph():
# app.run_server()
#         
# # createGraph()