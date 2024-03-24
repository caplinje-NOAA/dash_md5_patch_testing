# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 09:07:20 2024

@author: jim

Basic callback dashboard from:
https://dash.plotly.com/basic-callbacks
Modified to allow duplicate callbacks, with create_callback_id monkey patched
into dash.callback.  This was tested and works in a properly configured FIPS
environment. 

"""


from dash import Dash, dcc, html, Input, Output
import hashlib
import time


## define method that needs to be overloaded, copied from dash._utils
def create_callback_id(output, inputs):
   
    # A single dot within a dict id key or value is OK
    # but in case of multiple dots together escape each dot
    # with `\` so we don't mistake it for multi-outputs
    hashed_inputs = None

    def _concat(x):
        nonlocal hashed_inputs
        _id = x.component_id_str().replace(".", "\\.") + "." + x.component_property
        if x.allow_duplicate:
            if not hashed_inputs:
                #print('hash algo called')
                hashed_inputs = hashlib.sha512(
                    ".".join(str(x) for x in inputs).encode("utf-8")
                ).hexdigest()
            # Actually adds on the property part.
            _id += f"@{hashed_inputs}"
        return _id

    if isinstance(output, (list, tuple)):
        return ".." + "...".join(_concat(x) for x in output) + ".."

    return _concat(output)

# Monkey patched callback import
import dash
dash._callback.create_callback_id = create_callback_id
callback = dash.callback
N=10000

def noutputs(n):
    outs = []
    for i in range(n):
        outs.append(html.Div(id=f'my-output-{i}'))
        
    return html.Div(outs)

app = Dash(__name__,prevent_initial_callbacks=True)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    noutputs(N),

])

def callbackgen(n):
    outs = Output(component_id=f'my-output-{n}', component_property='children',allow_duplicate=True)
    ins = Input(component_id='my-input', component_property='value')
    @callback(
        outs,
        ins,
        prevent_initial_call=True
    )
    def nthCallback(input_value):
        return f'Output: {input_value}'
    
    return nthCallback,outs,ins

# register callbacks
s = time.time()
for i in range(N):
    nthCallback,outs,ins = callbackgen(i)
    #app.callback(output=outs,inputs=ins,prevent_initial_call=True)(nthCallback)

e = time.time()
print(f'dt = {e-s} s')
# if __name__ == '__main__':
#     app.run(debug=True)