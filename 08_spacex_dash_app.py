# Import required libraries
import pandas as pd
from dash import dcc,html,Dash
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("~/OneDrive/Desktop/data-science-pro-cert/08_capstone/files/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                        options=[{"label":"All Sites", "value":"ALL"}] + [{'label': site, 'value': site} for site in set(spacex_df['Launch Site'].values)], 
                                        value='ALL',
                                        placeholder="Launch Site",
                                        searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0', 10000: '10000'},    
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(launch_site):
    if launch_site == "ALL":
        filtered_df = spacex_df.groupby(["Launch Site"], as_index=False)[['Launch Site','class']].sum()
        filtered_df.columns = ["Launch Site", "Succesful Launches"]
        fig = px.pie(filtered_df, values='Succesful Launches',
                            names='Launch Site', title="Total Success Launches By Site")

        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==launch_site].groupby(['class'], as_index=False)['Launch Site'].count()
        filtered_df.columns = ["Launch Outcome","Launches"]
        fig = px.pie(filtered_df, values='Launches',
                            names="Launch Outcome", title="Launches Outcome for Site {}".format(launch_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_pie_chart(launch_site, payload_range):
    payload_min = payload_range[0]
    payload_max = payload_range[1]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > payload_min) & (spacex_df['Payload Mass (kg)'] < payload_max)]
    if launch_site == "ALL":
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==launch_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
