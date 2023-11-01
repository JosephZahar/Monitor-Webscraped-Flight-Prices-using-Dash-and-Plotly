from dash import html, dcc
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc

# Connect to your app pages
from src.pages import Analytics
from src.pages.Analytics import flight_scrapper_dash

# Connect the navbar to the index
from src.components import navbar

# Define the navbar
nav = navbar.Navbar()

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.7"}],
                external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

# Create the callback to handle multi-page inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return Analytics.layout


@app.callback([Output(component_id="indicators_flights", component_property="figure"),
               Output(component_id="fig1", component_property="figure"),
               Output(component_id="fig2", component_property="figure"),
               Output(component_id="fig3", component_property="figure"),
               Output(component_id="fig4", component_property="figure"),
               Output(component_id="fig5", component_property="figure")],
              [Input(component_id="departure_date", component_property="value"),
               Input(component_id="return_date", component_property="value")])
def callback_function(departure_date, return_date):
    indicators_flights, fig1, fig2, fig3, fig4, fig5 = flight_scrapper_dash(departure_date, return_date)
    return indicators_flights, fig1, fig2, fig3, fig4, fig5

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
