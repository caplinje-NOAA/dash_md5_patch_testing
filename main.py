# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 16:00:12 2024

@author: caplinje

Basic callback dashboard from:
https://dash.plotly.com/basic-callbacks
Modified to allow duplicate callbacks, which forces callbacks to use hash.md5
and therefore fails in a properly configured FIPS environment
"""

from dash import Dash, dcc, html, Input, Output, callback



app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),

])


@callback(
    Output(component_id='my-output', component_property='children',allow_duplicate=True),
    Input(component_id='my-input', component_property='value'),
    prevent_initial_call=True
)
def update_output_div(input_value):
    return f'Output: {input_value}'


if __name__ == '__main__':
    app.run(debug=True)