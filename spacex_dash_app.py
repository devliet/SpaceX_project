{
    "cells": [
        {
            "cell_type": "code",
            "execution_count": null,
            "metadata": {
                "collapsed": true
            },
            "outputs": [],
            "source": "# Import required libraries\nimport pandas as pd\nimport dash\nimport dash_html_components as html\nimport dash_core_components as dcc\nfrom dash.dependencies import Input, Output\nimport plotly.express as px\n\n# Read the airline data into pandas dataframe\nspacex_df = pd.read_csv(\"spacex_launch_dash.csv\")\nmax_payload = spacex_df['Payload Mass (kg)'].max()\nmin_payload = spacex_df['Payload Mass (kg)'].min()\n\n# print('##', spacex_df[spacex_df['class']==1] )\n# print(spacex_df[spacex_df['class']==1].groupby(['Launch Site']).head())\n\n\nb = [{'label': 'All Sites', 'value': 'ALL'}]\nc = [{'label':launchsite, 'value': launchsite}  for launchsite in spacex_df['Launch Site'].unique()]\nb.extend(c)\n\ndef compute_data_choice_1(df):\n    \n    pie_data1 = df[df['class']==1].groupby(['Launch Site'])\n    \n    pie_data2 = pie_data1['class'].sum().reset_index()\n    return pie_data2\n\n\ndef compute_data_choice_2(df, entered_site):\n    filtered_df = df[df['Launch Site']==entered_site].groupby(['class'])['Launch Site'].count().reset_index()\n    return filtered_df\n\n# Create a dash application\napp = dash.Dash(__name__)\n\n# Create an app layout\napp.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',\n                                        style={'textAlign': 'center', 'color': '#503D36',\n                                               'font-size': 40}),\n                                # TASK 1: Add a dropdown list to enable Launch Site selection\n                                # The default select value is for ALL sites\n                                # dcc.Dropdown(id='site-dropdown',...)\n                                dcc.Dropdown(id='site-dropdown',\n                                options=b,\n                                value='ALL',\n                                placeholder=\"Select a Launch Site here\",\n                                searchable=True\n                                ),\n                                html.Br(),\n\n                                # TASK 2: Add a pie chart to show the total successful launches count for all sites\n                                # If a specific launch site was selected, show the Success vs. Failed counts for the site\n                                \n                                html.Div(dcc.Graph(id='success-pie-chart')),\n                                html.Br(),\n\n                                html.P(\"Payload range (Kg):\"),\n                                # TASK 3: Add a slider to select payload range\n                                #dcc.RangeSlider(id='payload-slider',...)\n                                dcc.RangeSlider(id='payload-slider',  min=0, max=10000, step=2500,\n                                #marks={0: '0', 1000: '1000'},\n                                marks={i: str(i) for i in range(0,10001, 2500)},\n                                # value=[min_payload,max_payload]\n                                value=[5000,7000]\n                                ),\n                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success\n                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n                                ])\n\n# TASK 2:\n# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output\n# Function decorator to specify function input and output\n@app.callback(Output(component_id='success-pie-chart', component_property='figure'),\n              Input(component_id='site-dropdown', component_property='value'))\ndef get_pie_chart(entered_site):\n       \n    df =  spacex_df\n    \n    if entered_site == 'ALL':\n        pie_data = compute_data_choice_1(df)\n        print(pie_data.head())\n        pie_fig = px.pie(pie_data, values='class', names='Launch Site',  title='Correlation between payload mass and success for all launch sites')\n        \n    else:\n        # return the outcomes piechart for a selected site\n        pie_data = compute_data_choice_2(df, entered_site)\n        print(pie_data.head())\n        pie_fig = px.pie(pie_data, values='Launch Site', names='class', title='Class count for launchsite ' + entered_site)\n    \n    return pie_fig\n# TASK 4:\n# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output\n@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),\n              [Input(component_id='payload-slider', component_property='value'),\n              Input(component_id='site-dropdown', component_property='value')],\n              )\n\ndef set_slider(payload, entered_site):\n    df =  spacex_df\n    if entered_site == 'ALL':\n        scatter_dat  = df[['Payload Mass (kg)', 'class', 'Booster Version Category']]\n        \n    else:\n        scatter_dat = df[df['Launch Site']==entered_site]\n    \n    scatter_data = scatter_dat[(scatter_dat['Payload Mass (kg)'] >= payload[0]) & (scatter_dat['Payload Mass (kg)'] <= payload[1])]\n    scatter_fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color=\"Booster Version Category\")\n    return scatter_fig\n# Run the app\nif __name__ == '__main__':\n    app.run_server()\n"
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3.9",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.7"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 1
}