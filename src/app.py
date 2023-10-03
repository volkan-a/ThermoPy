'''
 # @ Create Time: 2023-10-03 18:28:47.423965
'''

from dash import Dash, callback, Input, Output, State
import dash_mantine_components as dmc
import CoolProp as cp
from numpy.random import randint
from dash_iconify import DashIconify

FLUIDS = cp.__fluids__
PROPERTIES = [
    {"value": "T", "label": "Temperature"},
    {"value": "P", "label": "Pressure"},
    {"value": "D", "label": "Density"},
    {"value": "U", "label": "Internal energy"},
    {"value": "H", "label": "Enthalpy"},
    {"value": "S", "label": "Entropy"},
    {"value": "Q", "label": "Quality"},
]

toto = randint(0, 20)

app = Dash(__name__, title="ThermoPy")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

app.layout = dmc.Center(
    # size="sm",
    children=[
        dmc.Stack(
            children=[
                dmc.Select(
                    id="fluid-select",
                    label="Select fluid",
                    placeholder="Select fluid",
                    value="Water",
                    data=[{"value": f, "label": f} for f in FLUIDS],
                    searchable=True,
                ),
                dmc.Group(
                    children=[
                        dmc.Select(
                            id="prop1-select",
                            label="Select first property",
                            placeholder="Select property",
                            value="T",
                            data=PROPERTIES,
                        ),
                        dmc.NumberInput(
                            id="prop1-value",
                            label="Value",
                            value=300,
                        ),
                    ]
                ),
                dmc.Group(
                    children=[
                        dmc.Select(
                            id="prop2-select",
                            label="Select second property",
                            placeholder="Select property",
                            value="P",
                            data=PROPERTIES,
                        ),
                        dmc.NumberInput(
                            id="prop2-value",
                            label="Value",
                            value=100000,
                        ),
                    ]
                ),
                dmc.Container(
                    children=dmc.Button("Calculate", size="xs", id="calculate-button"),
                ),
                dmc.Text(id="result", size="sm"),
                dmc.Text(f"toto = {toto}", size="sm"),
            ]
        )
    ],
)


@callback(
    Output("result", "children"),
    Input("calculate-button", "n_clicks"),
    State("fluid-select", "value"),
    State("prop1-select", "value"),
    State("prop1-value", "value"),
    State("prop2-select", "value"),
    State("prop2-value", "value"),
)
def update_text(n_clicks, fluid, prop1, value1, prop2, value2):
    """Update text based on checkbox"""
    return f'PropsSI("{prop1}", "{prop1}", {value1}, "{prop2}", {value2}, "{fluid}")'


if __name__ == "__main__":
    app.run_server(debug=True)
