# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:/Users/Chris/Desktop/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                    # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 ],
                                             value='ALL',
                                             placeholder="place holder here",
                                             searchable=True
                                             ),
                                html.Br(),

                    # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),
                                html.P("Payload Range (Kg):"),
                                
                                
                    # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(
                                   min=0,max=10000,step=1000,
                                   value=[min_payload,max_payload],
                                   id='payload-slider'),
                                   ),   

                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')), 
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site_dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df_pie = spacex_df.groupby(spacex_df["Launch Site"])["class"].sum().reset_index("Launch Site")
        fig = px.pie(df_pie, values='class', 
        names='Launch Site', 
        title='Successful Landings by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        df_pie =  spacex_df[spacex_df["Launch Site"]==entered_site]
        df_pie = df_pie.groupby(['Launch Site', 'class']).size().reset_index()
        df_pie = df_pie.rename(columns={0:'Count'})
        fig = px.pie(df_pie, values='Count', 
        names='class', 
        title='Success/Fail for '+entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site_dropdown', component_property='value'),
                 Input(component_id='payload-slider', component_property='value')])

def range_scatter(entered_site, loadrange):
    low,high = (loadrange[0], loadrange[1])
    df_slide = spacex_df[spacex_df["Payload Mass (kg)"].between(low,high)]
    
    if entered_site == 'ALL':
        fig = px.scatter(df_slide, x="Payload Mass (kg)",
                y="class", color="Booster Version Category", title="Payload vs. Outcome, All Sites")
        return fig
    else:
        # return the outcomes piechart for a selected site
        df_scat = df_slide[df_slide["Launch Site"]==entered_site]
        fig = px.scatter(df_scat, x="Payload Mass (kg)",
                y="class", color="Booster Version Category", title="Payload vs. Outcome by Booster, "+entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
