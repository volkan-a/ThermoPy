"""
 # @ Create Time: 2023-10-03 18:28:47.423965
"""

from dash import Dash, callback, Input, Output, State, html
import dash_mantine_components as dmc
from CoolProp.CoolProp import PropsSI
import CoolProp as cp


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

header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Property"),
                html.Th("Value"),
                html.Th("Unit"),
            ]
        )
    )
]

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
def update_text(
    n_clicks, fluid: str, prop1: str, value1: float, prop2: str, value2: float
):
    """Update text based on checkbox"""
    temperature = PropsSI("T", prop1, value1, prop2, value2, fluid)
    pressure = PropsSI("P", prop1, value1, prop2, value2, fluid)
    density = PropsSI("D", prop1, value1, prop2, value2, fluid)
    enthalpy = PropsSI("H", prop1, value1, prop2, value2, fluid)
    entropy = PropsSI("S", prop1, value1, prop2, value2, fluid)
    vapor_fraction = PropsSI("Q", prop1, value1, prop2, value2, fluid)

    row1 = html.Tr([html.Td("Temperature"), html.Td(temperature), html.Td("K")])
    row2 = html.Tr([html.Td("Pressure"), html.Td(pressure), html.Td("Pa")])
    row3 = html.Tr([html.Td("Density"), html.Td(density), html.Td("kg/m^3")])
    row4 = html.Tr([html.Td("Enthalpy"), html.Td(enthalpy), html.Td("J/kg")])
    row5 = html.Tr([html.Td("Entropy"), html.Td(entropy), html.Td("J/kg/K")])
    row6 = html.Tr([html.Td("Vapor fraction"), html.Td(vapor_fraction), html.Td("")])
    body = [html.Tbody([row1, row2, row3, row4, row5, row6])]
    return dmc.Table(header + body)


if __name__ == "__main__":
    app.run_server(debug=True)
