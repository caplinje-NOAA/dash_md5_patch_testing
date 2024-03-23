# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 09:07:20 2024

@author: jim

Blank dash project for testing hash.md5 swap with hash.sha256

"""

from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Hello World')
])

if __name__ == '__main__':
    app.run(debug=True)