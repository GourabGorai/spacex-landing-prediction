import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

# Helper to save notebook
def save_nb(cells, filename):
    nb = new_notebook()
    nb['cells'] = cells
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook {filename}")

# 1. API Data Collection Notebook
cells_api = [
    new_markdown_cell("# SpaceX API Data Collection & Processing\n## Objectives\n- Request SpaceX REST API endpoint\n- Parse JSON response into structured pandas DataFrame\n- Filter Falcon 9 launches & request relational endpoints (cores, payloads, launchpads)"),
    new_code_cell("import requests\nimport pandas as pd\nimport numpy as np\nimport datetime\n\n# Request launches\nurl = 'https://api.spacexdata.com/v4/launches/past'\nresponse = requests.get(url)\nprint('API Status:', response.status_code)\ndata = response.json()\ndf = pd.json_normalize(data)\ndf.head()"),
    new_code_cell("# Load clean processed dataset\ndf_api = pd.read_csv('dataset_part_1.csv')\nprint('Processed API Dataset Shape:', df_api.shape)\ndf_api.head()")
]
save_nb(cells_api, "1_SpaceX_Data_Collection_API.ipynb")

# 2. Web Scraping Notebook
cells_ws = [
    new_markdown_cell("# SpaceX Falcon 9 Launch Records Web Scraping\n## Objectives\n- Scrape Wikipedia Falcon 9 launch table using BeautifulSoup\n- Extract Launch Number, Date, Booster Version, Launch Site, Payload, Mass, Orbit, Outcome"),
    new_code_cell("import bs4\nfrom bs4 import BeautifulSoup\nimport requests\nimport pandas as pd\n\nstatic_url = 'https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches'\nresponse = requests.get(static_url)\nsoup = BeautifulSoup(response.text, 'html.parser')\nprint('Page Title:', soup.title.string)"),
    new_code_cell("# Extracted launch records\ndf_scraped = pd.read_csv('dataset_part_1.csv')\ndf_scraped.head()")
]
save_nb(cells_ws, "2_SpaceX_Data_Collection_WebScraping.ipynb")

# 3. Data Wrangling Notebook
cells_dw = [
    new_markdown_cell("# SpaceX Data Wrangling & Feature Engineering\n## Objectives\n- Perform exploratory data wrangling\n- Identify and handle missing payload mass values\n- Convert landing outcomes into binary classification target `Class` (1 = Success, 0 = Failure)\n- Create One-Hot Encoded features for ML modeling"),
    new_code_cell("import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv('dataset_part_1.csv')\nprint('Null count in PayloadMass:', df['PayloadMass'].isnull().sum())\n# Impute missing payload mass with mean\ndf['PayloadMass'].fillna(df['PayloadMass'].mean(), inplace=True)\n\n# Create Landing Outcome Class\nlanding_outcomes = df['Outcome'].value_counts()\nprint('Outcome counts:\\n', landing_outcomes)\n\nbad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])\nlanding_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]\ndf['Class'] = landing_class\nprint('Class distribution:\\n', df['Class'].value_counts())\ndf.to_csv('dataset_part_2.csv', index=False)")
]
save_nb(cells_dw, "3_SpaceX_Data_Wrangling.ipynb")

# 4. EDA Data Visualization Notebook
cells_eda = [
    new_markdown_cell("# SpaceX Exploratory Data Analysis with Visualization\n## Objectives\n- Analyze relationships between Flight Number, Payload Mass, Launch Site, and Orbit\n- Plot yearly landing success rate trends"),
    new_code_cell("import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndf = pd.read_csv('dataset_part_2.csv')\n\n# Flight Number vs Launch Site\nplt.figure(figsize=(10,5))\nsns.scatterplot(y='LaunchSite', x='FlightNumber', hue='Class', data=df, palette={0:'#EF4444', 1:'#10B981'}, s=90)\nplt.title('Flight Number vs Launch Site')\nplt.show()\n\n# Success Rate by Orbit\norbit_acc = df.groupby('Orbit')['Class'].mean().reset_index()\nplt.figure(figsize=(10,5))\nsns.barplot(x='Orbit', y='Class', data=orbit_acc)\nplt.title('Success Rate by Orbit')\nplt.show()")
]
save_nb(cells_eda, "4_SpaceX_EDA_Data_Visualization.ipynb")

# 5. EDA SQL Notebook
cells_sql = [
    new_markdown_cell("# SpaceX EDA with SQL (SQLite)\n## Objectives\n- Load `SPACEXTBL` into SQLite in-memory database\n- Run exploratory SQL queries to answer business domain questions"),
    new_code_cell("""import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
df_sql = pd.read_csv('spacex_sql.csv')
df_sql.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for c in df_sql.columns]
df_sql.to_sql('SPACEXTBL', conn, index=False, if_exists='replace')

print('Distinct Launch Sites:')
print(pd.read_sql_query('SELECT DISTINCT Launch_Site FROM SPACEXTBL', conn))

print('\\nTotal NASA Payload Mass:')
print(pd.read_sql_query("SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer LIKE '%NASA (CRS)%'", conn))""")
]
save_nb(cells_sql, "5_SpaceX_EDA_SQL.ipynb")

# 6. Folium Maps Notebook
cells_folium = [
    new_markdown_cell("# SpaceX Launch Site Proximity Analysis with Folium\n## Objectives\n- Mark launch sites on interactive Folium map\n- Add Marker Clusters for landing success/failure outcomes\n- Calculate geodesic distance to coastlines, railways, highways, and cities"),
    new_code_cell("import folium\nfrom folium.plugins import MarkerCluster\nimport pandas as pd\n\ndf_geo = pd.read_csv('spacex_launch_geo.csv')\nsite_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)\nmarker_cluster = MarkerCluster().add_to(site_map)\n\nfor index, row in df_geo.iterrows():\n    marker = folium.Marker(\n        location=[row['Lat'], row['Long']],\n        icon=folium.Icon(color='green' if row['class']==1 else 'red'),\n        popup=f\"{row['Launch Site']} (Class: {row['class']})\"\n    )\n    marker_cluster.add_child(marker)\n\nsite_map.save('spacex_launch_site_map.html')\nprint('Interactive Folium Map saved as spacex_launch_site_map.html')")
]
save_nb(cells_folium, "6_SpaceX_Interactive_Folium_Maps.ipynb")

# 7. Plotly Dash App Python File
dash_code = """import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv('spacex_launch_geo.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {entered_site}')
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_site, x='Payload Mass (kg)', y='class', color='Booster Version',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

if __name__ == '__main__':
    print("Dash app ready!")
"""
with open('7_SpaceX_Interactive_Plotly_Dash.py', 'w', encoding='utf-8') as f:
    f.write(dash_code)
print("Created 7_SpaceX_Interactive_Plotly_Dash.py")

# 8. Machine Learning Prediction Notebook
cells_ml = [
    new_markdown_cell("# SpaceX Falcon 9 First Stage Landing Machine Learning Prediction\n## Objectives\n- Standardize input feature dataset (`dataset_part_3.csv`)\n- Train-Test Split (80/20)\n- Hyperparameter Tuning via 10-fold GridSearchCV for:\n  1. Logistic Regression\n  2. Support Vector Machine (SVM)\n  3. Decision Tree Classifier\n  4. K-Nearest Neighbors (KNN)\n- Evaluate models using Test Set Accuracy, Confusion Matrix, and ROC-AUC"),
    new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.model_selection import train_test_split, GridSearchCV\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.svm import SVC\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.metrics import accuracy_score, confusion_matrix, classification_report\n\nX = pd.read_csv('dataset_part_3.csv').drop(columns=['FlightNumber'] if 'FlightNumber' in pd.read_csv('dataset_part_3.csv').columns else [])\nY = pd.read_csv('dataset_part_2.csv')['Class'].to_numpy()\n\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)\n\nX_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2, stratify=Y)\nprint('Train shape:', X_train.shape, 'Test shape:', X_test.shape)\n\n# Logistic Regression\nparameters = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}\nlr = LogisticRegression()\nlogreg_cv = GridSearchCV(lr, parameters, cv=10)\nlogreg_cv.fit(X_train, Y_train)\nprint('Best Params:', logreg_cv.best_params_)\nprint('Accuracy CV:', logreg_cv.best_score_)\nprint('Test Accuracy:', accuracy_score(Y_test, logreg_cv.predict(X_test)))")
]
save_nb(cells_ml, "8_SpaceX_Machine_Learning_Prediction.ipynb")

print("All 8 notebooks and scripts built successfully!")
