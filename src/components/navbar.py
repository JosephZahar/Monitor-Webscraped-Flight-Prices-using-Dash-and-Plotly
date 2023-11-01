from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Analytics", href="/Analytics", id="Analytics")),
            ] ,
            brand="Flights Scrapper Dashboard",
            brand_href="/Analytics",
            id="navbar",
            color="dark",
            dark=True,
            brand_style={'fontSize': '30px', 'textAlign': 'center', 'width': '100%'},
        ),
    ])

    return layout