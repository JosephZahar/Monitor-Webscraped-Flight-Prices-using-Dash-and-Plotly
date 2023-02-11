# import desired libraries
import calendar
from datetime import date, timedelta

import pandas as pd
import plotly.io as pio

pio.templates.default = "simple_white"

import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import warnings

warnings.filterwarnings("ignore")

flights_df = pd.read_csv("/Users/macbookpro/PycharmProjects/Airline Webscrapper/webscrapped_flights.csv")
flights_df['timestamp'] = pd.to_datetime(flights_df['timestamp']).dt.date
flights_df['price'] = flights_df.price.apply(lambda row: int(row.replace(",", "")))
unfiltered_dep_df = flights_df[flights_df.type == 'Departure']
unfiltered_ret_df = flights_df[flights_df.type == 'Return']


def flight_scrapper_dash(departure_date, return_date):
    df = flights_df.copy()
    if departure_date != 'All' and return_date != 'All':
        df = df[df.flight_date.str.contains([departure_date, return_date])]
    elif departure_date != 'All':
        df = df[df.flight_date.str.contains(departure_date)]
    elif return_date != 'All':
        df = df[df.flight_date.str.contains(return_date)]
    else:
        df = df.copy()

    today = date.today()
    week_prior = today - timedelta(weeks=1)

    departure_df = df[df.type == 'Departure']
    return_df = df[df.type == 'Return']
    tot_df = df[df.type == 'Total']

    prev_week_df = tot_df[tot_df['timestamp'] <= week_prior]
    prev_week_min = prev_week_df.price.min()
    prev_week_max = prev_week_df.price.min()

    indicators_flights= go.Figure()
    indicators_flights.add_trace(go.Indicator(
        mode="number+delta",
        value=tot_df.price.min(),
        number={'suffix': " $", "font":{"size":50}},
        title={"text": f"<br><span style=';color:black'> Lowest Flight Price <br> {tot_df[tot_df.price == tot_df.price.min()].flight_date.values[0]}  </span>",
               "font": { "size": 20 }},
        delta = {'reference': prev_week_min, 'relative': True},
        domain={'row': 0, 'column': 0}))

    indicators_flights.add_trace(go.Indicator(
        mode="number+delta",
        value=tot_df.price.max(),
        number={'suffix': " $", "font":{"size":50}},
        title={"text": f"<br><span style=';color:black'> Highest Flight Price <br> {tot_df[tot_df.price == tot_df.price.max()].flight_date.values[0]} </span>",
               "font": { "size": 20 }},
        delta={'reference': prev_week_max, 'relative': True},
        domain={'row': 0, 'column': 1}))

    indicators_flights.add_trace(go.Indicator(
        mode="number",
        value=departure_df.price.mean(),
        number={'suffix': " $", "font":{"size":50}},
        title={"text": "<br><span style=';color:black'> Average Departure <br> Price </span>",
               "font": {"size": 20}},
        domain={'row': 0, 'column': 2}))

    indicators_flights.add_trace(go.Indicator(
        mode="number",
        value=return_df.price.mean(),
        number={'suffix': " $", "font":{"size":50}},
        title={"text": "<br><span style=';color:black'> Average Return <br> Price </span>",
               "font": {"size": 20}},
        domain={'row': 0, 'column': 3}))

    indicators_flights.add_trace(go.Indicator(
        mode="number",
        number={'prefix': f"{calendar.day_name[df[df.price==departure_df.price.min()]['timestamp'].values[0].weekday()]}"},
        title={"text": f"<br><span style=';color:black'> Optimal Booking <br> Day </span>",
               "font": {"size": 20}},
        domain={'row': 0, 'column': 4}))

    indicators_flights.update_layout(
        grid={'rows': 1, 'columns': 5, 'pattern': "independent"},
        margin=dict(l=10, r=10, t=10, b=10))

    avg_prices = df.groupby('type')['price'].mean().T
    data = pd.DataFrame({'Price': [round(avg_prices['Departure'],2), round(avg_prices['Return'],2), round(avg_prices['Total'],2)],
                         'Label': ["Departure", "Return", "Roundtrip"],
                         'colors': ["cornflowerblue", "red", "greenyellow"]})

    data = data.sort_values(['Price'], ascending=False)
    fig1 = go.Figure(go.Sunburst(
        labels=data['Label'].values,
        parents=[""] + list(data['Label'][:-1]),
        values=data['Price'].values,
        branchvalues='total',
        marker=dict(colors=data['colors'].values))
    )
    fig1.update_layout(showlegend=False)
    fig1.update_layout(title="Hierarchical Price Composition")


    fig2 = go.Figure()
    fig2.add_trace(go.Box(x=tot_df['price'], name='Roundtrip Flights',
                          fillcolor='greenyellow',
                          marker_color='greenyellow',
                          customdata=tot_df['flight_date'],
                          line={"color": "black"},
                          hovertemplate='Flight Date: %{customdata}<extra></extra>',
                          boxpoints='all'))
    fig2.add_trace(go.Box(x=return_df['price'], name='Return Flights',
                          fillcolor='red',
                          marker_color='red',
                          customdata=return_df['flight_date'],
                          line={"color": "black"},
                          hovertemplate='Flight Date: %{customdata}<extra></extra>',
                          boxpoints='all'))
    fig2.add_trace(go.Box(x=departure_df['price'], name='Departure Flights',
                          fillcolor='cornflowerblue',
                          marker_color='cornflowerblue',
                          customdata=departure_df['flight_date'],
                          line={"color": "black"},
                          hovertemplate='Flight Date: %{customdata}<extra></extra>',
                          boxpoints='all'))


    fig2.update_layout(boxmode='group', showlegend=False)
    fig2.update_traces(orientation='h')
    fig2.update_layout(hovermode="y unified")
    fig2.update_layout(title="Price Distribution per Category",
                       xaxis_title="Price ($)",)


    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=unfiltered_dep_df['flight_date'],
        y=unfiltered_dep_df['price'],
        marker_color='cornflowerblue',
        histfunc='avg',
    ))
    fig3.update_layout(title="Average Departure Date Price",
    xaxis_title="Departure Date",
    yaxis_title="Average Price ($)",
    bargap=0.6)
    fig3.update_xaxes(tickangle=25)


    fig4 = go.Figure()
    fig4.add_trace(go.Histogram(
        x=unfiltered_ret_df['flight_date'],
        y=unfiltered_ret_df['price'],
        marker_color='red',
        histfunc='avg',
    ))
    fig4.update_layout(title="Average Return Date Price",
                       xaxis_title="Return Date",
                       yaxis_title="Average Price ($)",
                       bargap=0.6)
    fig4.update_xaxes(tickangle=25)


    return indicators_flights, fig1, fig2, fig3, fig4



indicators_flights, fig1, fig2, fig3, fig4 = flight_scrapper_dash('All', 'All', )

departure_dropdown = dcc.Dropdown(options=list(set([i for i in unfiltered_dep_df['flight_date']])) + ['All'],
                                  id='departure_date',
                                  clearable=False,
                                  value='All', className="dbc",
                                  placeholder='Select a Departure Date', maxHeight=100)

return_dropdown = dcc.Dropdown(options=list(set([i for i in unfiltered_ret_df['flight_date']])) + ['All'],
                               id='return_date',
                               clearable=False,
                               value='All', className="dbc",
                               placeholder='Select a Return Date', maxHeight=100)

layout = dbc.Container(
    [dbc.Row([dbc.Col(departure_dropdown),
              dbc.Col(return_dropdown),]),
     dbc.Row([
         dbc.Col([
             dcc.Graph(id='indicators_flights', figure=indicators_flights,
                       style={'height': 300}),
             html.Hr()
         ], width={'size': 12, 'offset': 0, 'order': 1})]),

     dbc.Row([dbc.Col([
             dcc.Graph(id='fig1', figure=fig1,
                       style={'height': 500}),
             html.Hr()
         ], width={'size': 6, 'offset': 0, 'order': 1}),
         dbc.Col([
             dcc.Graph(id='fig2', figure=fig2,
                       style={'height': 500}),
             html.Hr()
         ], width={'size': 6, 'offset': 0, 'order': 2})]),

     dbc.Row([dbc.Col([
             dcc.Graph(id='fig3', figure=fig3,
                       style={'height': 400}),
             html.Hr()
         ], width={'size': 6, 'offset': 0, 'order': 1}),
         dbc.Col([
             dcc.Graph(id='fig4', figure=fig4,
                       style={'height': 400}),
             html.Hr()
         ], width={'size': 6, 'offset': 0, 'order': 2})]
    )]
)
