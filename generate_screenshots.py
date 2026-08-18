import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('historical_automobile_sales.csv')

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

def generate_recession_dashboard_image():
    recession_data = df[df['Recession'] == 1]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Automobile Sales Statistics Dashboard - Recession Period Report', fontsize=18, fontweight='bold', color='#503D36', y=0.98)
    
    # 1. Sales Fluctuation Line Plot
    yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    axes[0, 0].plot(yearly_rec['Year'], yearly_rec['Automobile_Sales'], marker='o', color='#2b5c8f', linewidth=2.5)
    axes[0, 0].set_title('Automobile Sales Fluctuation Over Recession Period', fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Average Automobile Sales')
    axes[0, 0].grid(True, linestyle='--')
    
    # 2. Avg Sales by Vehicle Type Bar Chart
    avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    sns.barplot(ax=axes[0, 1], data=avg_sales, x='Vehicle_Type', y='Automobile_Sales', palette='Blues_r')
    axes[0, 1].set_title('Average Vehicles Sold by Vehicle Type During Recessions', fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel('Vehicle Type')
    axes[0, 1].set_ylabel('Average Automobile Sales')
    axes[0, 1].tick_params(axis='x', rotation=15)
    
    # 3. Advertising Expenditure Share Pie Chart
    exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    axes[1, 0].pie(exp_rec['Advertising_Expenditure'], labels=exp_rec['Vehicle_Type'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Pastel1'))
    axes[1, 0].set_title('Total Advertising Expenditure Share by Vehicle Type', fontsize=13, fontweight='bold')
    
    # 4. Unemployment Effect Bar/Line Chart
    unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
    sns.barplot(ax=axes[1, 1], data=unemp_data, x='unemployment_rate', y='Automobile_Sales', hue='Vehicle_Type', palette='tab10')
    axes[1, 1].set_title('Effect of Unemployment Rate on Vehicle Type and Sales', fontsize=13, fontweight='bold')
    axes[1, 1].set_xlabel('Unemployment Rate (%)')
    axes[1, 1].set_ylabel('Automobile Sales')
    axes[1, 1].legend(title='Vehicle Type', fontsize=9)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('recession_report_screenshot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("recession_report_screenshot.png created successfully!")

def generate_yearly_dashboard_image(year=2010):
    yearly_data = df[df['Year'] == year]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Automobile Sales Statistics Dashboard - Yearly Report ({year})', fontsize=18, fontweight='bold', color='#503D36', y=0.98)
    
    # 1. Overall Sales Fluctuation
    yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
    axes[0, 0].plot(yas['Year'], yas['Automobile_Sales'], marker='s', color='#2ca02c', linewidth=2)
    axes[0, 0].set_title('Yearly Automobile Sales Fluctuation (Overall)', fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Average Automobile Sales')
    axes[0, 0].grid(True, linestyle='--')
    
    # 2. Monthly Sales Line Chart for selected year
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
    mas['Month'] = pd.Categorical(mas['Month'], categories=month_order, ordered=True)
    mas = mas.sort_values('Month')
    
    axes[0, 1].plot(mas['Month'], mas['Automobile_Sales'], marker='o', color='#ff7f0e', linewidth=2.5)
    axes[0, 1].set_title(f'Total Monthly Automobile Sales in {year}', fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Total Automobile Sales')
    axes[0, 1].grid(True, linestyle='--')
    
    # 3. Average Vehicles Sold by Vehicle Type
    avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    sns.barplot(ax=axes[1, 0], data=avr_vdata, x='Vehicle_Type', y='Automobile_Sales', palette='Greens_r')
    axes[1, 0].set_title(f'Average Vehicles Sold by Vehicle Type in {year}', fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel('Vehicle Type')
    axes[1, 0].set_ylabel('Average Automobile Sales')
    axes[1, 0].tick_params(axis='x', rotation=15)
    
    # 4. Advertising Expenditure Pie Chart
    exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    axes[1, 1].pie(exp_data['Advertising_Expenditure'], labels=exp_data['Vehicle_Type'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))
    axes[1, 1].set_title(f'Total Advertisement Expenditure by Vehicle Type in {year}', fontsize=13, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('yearly_report_screenshot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("yearly_report_screenshot.png created successfully!")

if __name__ == '__main__':
    generate_recession_dashboard_image()
    generate_yearly_dashboard_image()
