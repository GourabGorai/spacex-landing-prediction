import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # TASK 4.1: Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 24
        }
    ),
    # TASK 4.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            disabled=True,
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),
    # TASK 4.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap'})
    ])
])

# TASK 4.4: Define the callback function to update the input container (enable/disable year dropdown)
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# TASK 4.5 & 4.6: Define the callback function to update the output container
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession period
        recession_data = data[data['Recession'] == 1]
        
        # TASK 4.5: Display graphs for Recession Report Statistics
        # Plot 1: Automobile Sales fluctuation over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, 
                x='Year', 
                y='Automobile_Sales',
                title="Automobile Sales Fluctuation Over Recession Period"
            )
        )

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales, 
                x='Vehicle_Type', 
                y='Automobile_Sales',
                title="Average Vehicles Sold by Vehicle Type During Recessions"
            )
        )
        
        # Plot 3: Total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, 
                values='Advertising_Expenditure', 
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recessions"
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data, 
                x='unemployment_rate', 
                y='Automobile_Sales', 
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales During Recessions"
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex', 'width': '100%'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex', 'width': '100%'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == int(input_year)]
        
        # TASK 4.6: Display graphs for Yearly Report Statistics
        # Plot 1: Yearly Automobile Sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, 
                x='Year', 
                y='Automobile_Sales',
                title="Yearly Automobile Sales Fluctuation (Overall)"
            )
        )
            
        # Plot 2: Total Monthly Automobile Sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        # Order months chronologically
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        mas['Month'] = pd.Categorical(mas['Month'], categories=month_order, ordered=True)
        mas = mas.sort_values('Month')
        
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas, 
                x='Month', 
                y='Automobile_Sales',
                title=f"Total Monthly Automobile Sales in {input_year}"
            )
        )

        # Plot 3: Average Vehicles Sold by Vehicle Type during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata, 
                x='Vehicle_Type', 
                y='Automobile_Sales',
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}"
            )
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle type using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, 
                values='Advertising_Expenditure', 
                names='Vehicle_Type',
                title=f"Total Advertisement Expenditure by Vehicle Type in {input_year}"
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex', 'width': '100%'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex', 'width': '100%'})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
