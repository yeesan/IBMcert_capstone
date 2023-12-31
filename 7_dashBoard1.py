'''
This project was ran in Skills Networks Labs IDE
install packages: python3.8 -m pip install pandas dash
get dataset : wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
run : python3.8 spacex_dash_app.py
'''
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
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
                                dcc.Dropdown(id='site-dropdown',  
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([], id='success-payload-scatter-chart')
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='children'),
              Input(component_id='site-dropdown', component_property='value'), 
              )
def get_pie_chart(entered_site):
        
    filtered_df = spacex_df[['Launch Site', 'class']] # filtered only necessary data

    if entered_site == 'ALL':
        data = filtered_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='pie chart by Launch Site')
        return dcc.Graph(figure=fig)

    else:
        data = filtered_df.loc[filtered_df['Launch Site']== entered_site]
        data = data.groupby(['class'])['Launch Site'].count().reset_index() 
        data = data.rename(columns={"Launch Site":"count"})
        fig = px.pie(data, values='count', 
        names='class', 
        title=entered_site)
        return dcc.Graph(figure=fig)

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='children'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")]              
              )
def get_scatter_chart(entered_site, entered_payload):
    
    filtered_df2 = spacex_df[['Launch Site', 'Payload Mass (kg)', 'Booster Version Category', 'class']] # filtered only necessary data
    lw, hi = entered_payload
    
    if entered_site == 'ALL':
        mask = (filtered_df2['Payload Mass (kg)']>=lw)& (filtered_df2['Payload Mass (kg)'] <= hi)
        fig2 = px.scatter(filtered_df2[mask], x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return dcc.Graph(figure=fig2)
    else:
        data2 = filtered_df2.loc[filtered_df2['Launch Site'] == entered_site].reset_index()
        mask = (data2['Payload Mass (kg)']>=lw)& (data2['Payload Mass (kg)'] <= hi)
        fig2 = px.scatter(data2[mask], x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return dcc.Graph(figure=fig2) 




# Run the app
if __name__ == '__main__':
    app.run_server()
