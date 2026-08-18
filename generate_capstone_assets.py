import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_curve, auc

# Set aesthetic styling
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8,
    'grid.color': '#eeeeee',
    'grid.linestyle': '--'
})

os.makedirs('assets', exist_ok=True)

# Load Datasets
df_part2 = pd.read_csv('dataset_part_2.csv')
df_part3 = pd.read_csv('dataset_part_3.csv')
df_geo = pd.read_csv('spacex_launch_geo.csv')
df_sql = pd.read_csv('spacex_sql.csv')

print("Datasets loaded successfully.")

# ----------------------------------------------------
# 1. EDA Visualization Charts
# ----------------------------------------------------

# Chart 1: Flight Number vs Launch Site
plt.figure(figsize=(10, 5))
sns.scatterplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df_part2, palette={0: "#EF4444", 1: "#10B981"}, s=90, alpha=0.9)
plt.title("Flight Number vs. Launch Site (Outcome Color-Coded)", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Flight Number", fontsize=11, fontweight='bold')
plt.ylabel("Launch Site", fontsize=11, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('assets/chart_1_flight_vs_launchsite.png', dpi=300)
plt.close()

# Chart 2: Payload Mass vs Launch Site
plt.figure(figsize=(10, 5))
sns.scatterplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df_part2, palette={0: "#EF4444", 1: "#10B981"}, s=90, alpha=0.9)
plt.title("Payload Mass (kg) vs. Launch Site", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Payload Mass (kg)", fontsize=11, fontweight='bold')
plt.ylabel("Launch Site", fontsize=11, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('assets/chart_2_payload_vs_launchsite.png', dpi=300)
plt.close()

# Chart 3: Success Rate per Orbit Type
orbit_success = df_part2.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
plt.figure(figsize=(10, 5))
colors = ['#10B981' if val >= 0.7 else '#F59E0B' if val >= 0.5 else '#EF4444' for val in orbit_success['Class']]
ax = sns.barplot(x='Orbit', y='Class', data=orbit_success, palette=colors)
plt.title("Success Rate by Orbit Type", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Orbit Type", fontsize=11, fontweight='bold')
plt.ylabel("Success Rate (0.0 - 1.0)", fontsize=11, fontweight='bold')
plt.ylim(0, 1.1)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points', fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_3_success_vs_orbit.png', dpi=300)
plt.close()

# Chart 4: Flight Number vs Orbit Type
plt.figure(figsize=(10, 5))
sns.scatterplot(y="Orbit", x="FlightNumber", hue="Class", data=df_part2, palette={0: "#EF4444", 1: "#10B981"}, s=90, alpha=0.9)
plt.title("Flight Number vs. Orbit Type", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Flight Number", fontsize=11, fontweight='bold')
plt.ylabel("Orbit Type", fontsize=11, fontweight='bold')
plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"], loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('assets/chart_4_flight_vs_orbit.png', dpi=300)
plt.close()

# Chart 5: Launch Success Yearly Trend
df_part2['Year'] = pd.to_datetime(df_part2['Date']).dt.year
yearly_success = df_part2.groupby('Year')['Class'].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(yearly_success['Year'], yearly_success['Class'], marker='o', color='#0284C7', linewidth=2.5, markersize=7)
plt.fill_between(yearly_success['Year'], yearly_success['Class'], color='#0284C7', alpha=0.15)
plt.title("Yearly Launch Success Rate Trend (2010 - 2020)", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Year", fontsize=11, fontweight='bold')
plt.ylabel("Average Success Rate", fontsize=11, fontweight='bold')
plt.ylim(-0.05, 1.1)
plt.xticks(yearly_success['Year'])
for x, y in zip(yearly_success['Year'], yearly_success['Class']):
    plt.annotate(f"{y*100:.0f}%", (x, y), ha='center', va='bottom', fontsize=9, xytext=(0, 5), textcoords='offset points', fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_5_yearly_success_trend.png', dpi=300)
plt.close()

# ----------------------------------------------------
# 2. SQL Analysis Execution
# ----------------------------------------------------
conn = sqlite3.connect(':memory:')
df_sql_clean = df_sql.copy()
df_sql_clean.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for c in df_sql_clean.columns]
df_sql_clean.to_sql('SPACEXTBL', conn, index=False, if_exists='replace')

sql_queries = {
    "Q1: Distinct Launch Sites": "SELECT DISTINCT Launch_Site FROM SPACEXTBL",
    "Q2: CCA Sites": "SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5",
    "Q3: NASA Payload Sum": "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_NASA_Payload FROM SPACEXTBL WHERE Customer LIKE '%NASA (CRS)%'",
    "Q4: F9 v1.1 Avg Payload": "SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload FROM SPACEXTBL WHERE Booster_Version LIKE '%F9 v1.1%'",
    "Q5: First Ground Pad Success": "SELECT MIN(Date) AS First_Ground_Success FROM SPACEXTBL WHERE Landing_Outcome LIKE '%Success (ground pad)%'",
    "Q6: Drone Ship Success 4-6k kg": "SELECT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000",
    "Q7: Mission Outcomes Count": "SELECT Mission_Outcome, COUNT(*) AS Count FROM SPACEXTBL GROUP BY Mission_Outcome",
    "Q8: Max Payload Boosters": "SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)",
    "Q9: 2015 Drone/Ground Failures": "SELECT strftime('%m', Date) AS Month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE strftime('%Y', Date) = '2015' AND Landing_Outcome LIKE '%Failure%'",
    "Q10: Ranked Outcomes 2010-2017": "SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC"
}

sql_results = {}
for q_name, query in sql_queries.items():
    res = pd.read_sql_query(query, conn)
    sql_results[q_name] = res

# ----------------------------------------------------
# 3. Interactive Visual Analytics Figures (Dash & Folium Mockup Graphics)
# ----------------------------------------------------

# Dash Chart 1: Success Pie Chart
plt.figure(figsize=(7, 5))
site_counts = df_geo[df_geo['class'] == 1]['Launch Site'].value_counts()
plt.pie(site_counts, labels=site_counts.index, autopct='%1.1f%%', startangle=140, colors=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'])
plt.title("Total Successful Launches by Launch Site", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_8_dash_pie_chart.png', dpi=300)
plt.close()

# Dash Chart 2: Payload vs Outcome Scatter
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df_geo, x='Payload Mass (kg)', y='class', hue='Booster Version', style='Booster Version', s=100, palette='Set1')
plt.title("Payload Mass vs. Launch Outcome (Booster Version Categories)", fontsize=12, fontweight='bold')
plt.xlabel("Payload Mass (kg)", fontsize=10, fontweight='bold')
plt.ylabel("Class (0 = Failure, 1 = Success)", fontsize=10, fontweight='bold')
plt.yticks([0, 1])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('assets/chart_9_dash_scatter_chart.png', dpi=300)
plt.close()

# Folium Map Graphic Simulation
plt.figure(figsize=(9, 5))
plt.scatter(df_geo['Long'], df_geo['Lat'], c=['#10B981' if c == 1 else '#EF4444' for c in df_geo['class']], s=80, alpha=0.8, edgecolors='black')
plt.title("Folium Interactive Map Simulation: Launch Site Clusters & Distances", fontsize=12, fontweight='bold')
plt.xlabel("Longitude", fontsize=10, fontweight='bold')
plt.ylabel("Latitude", fontsize=10, fontweight='bold')
sites = df_geo[['Launch Site', 'Lat', 'Long']].drop_duplicates()
for _, row in sites.iterrows():
    plt.annotate(row['Launch Site'], (row['Long'], row['Lat']), xytext=(5, 5), textcoords='offset points', fontweight='bold', fontsize=9, color='#1E293B')
plt.grid(True)
plt.tight_layout()
plt.savefig('assets/chart_7_folium_map.png', dpi=300)
plt.close()

# ----------------------------------------------------
# 4. Machine Learning Modeling
# ----------------------------------------------------
X = df_part3.drop(columns=['FlightNumber']) if 'FlightNumber' in df_part3.columns else df_part3
Y = df_part2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2, stratify=Y)

parameters_lr = {'C': [0.01, 0.1, 1, 10], 'penalty': ['l2'], 'solver': ['lbfgs']}
parameters_svm = {'kernel': ['linear', 'rbf', 'poly', 'sigmoid'], 'C': np.logspace(-3, 3, 5), 'gamma': np.logspace(-3, 3, 5)}
parameters_tree = {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [2*n for n in range(1, 10)], 'max_features': ['sqrt'], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}
parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}

models = {
    'Logistic Regression': (LogisticRegression(max_iter=1000), parameters_lr),
    'SVM': (SVC(probability=True), parameters_svm),
    'Decision Tree': (DecisionTreeClassifier(random_state=42), parameters_tree),
    'KNN': (KNeighborsClassifier(), parameters_knn)
}

model_results = {}
confusion_matrices = {}
roc_data = {}

for name, (model, params) in models.items():
    grid = GridSearchCV(model, params, cv=10)
    grid.fit(X_train, Y_train)
    best_model = grid.best_estimator_
    train_acc = grid.best_score_
    y_pred = best_model.predict(X_test)
    test_acc = accuracy_score(Y_test, y_pred)
    cm = confusion_matrix(Y_test, y_pred)
    
    if hasattr(best_model, "predict_proba"):
        y_prob = best_model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(Y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        roc_data[name] = (fpr, tpr, roc_auc)
    
    model_results[name] = {
        'best_params': grid.best_params_,
        'train_accuracy': train_acc,
        'test_accuracy': test_acc,
        'model': best_model
    }
    confusion_matrices[name] = cm
    print(f"{name} -> Train Acc (CV): {train_acc:.4f}, Test Acc: {test_acc:.4f}")

# Plot Confusion Matrices
fig, axes = plt.subplots(2, 2, figsize=(8, 7))
axes = axes.flatten()
for idx, (name, cm) in enumerate(confusion_matrices.items()):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False, annot_kws={'size': 14, 'weight': 'bold'})
    axes[idx].set_title(f"{name}\nTest Acc: {model_results[name]['test_accuracy']*100:.1f}%", fontsize=11, fontweight='bold')
    axes[idx].set_xlabel('Predicted Label', fontsize=9)
    axes[idx].set_ylabel('True Label', fontsize=9)
    axes[idx].set_xticklabels(['Failure (0)', 'Success (1)'])
    axes[idx].set_yticklabels(['Failure (0)', 'Success (1)'])

plt.tight_layout()
plt.savefig('assets/chart_10_confusion_matrices.png', dpi=300)
plt.close()

# Model Comparison Bar Chart
plt.figure(figsize=(9, 5))
names = list(model_results.keys())
train_scores = [model_results[n]['train_accuracy']*100 for n in names]
test_scores = [model_results[n]['test_accuracy']*100 for n in names]

x = np.arange(len(names))
width = 0.35

plt.bar(x - width/2, train_scores, width, label='Train Accuracy (10-fold CV)', color='#3B82F6')
plt.bar(x + width/2, test_scores, width, label='Test Accuracy', color='#10B981')

plt.title("Classification Model Performance Comparison", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Machine Learning Algorithm", fontsize=11, fontweight='bold')
plt.ylabel("Accuracy (%)", fontsize=11, fontweight='bold')
plt.xticks(x, names, fontweight='bold')
plt.ylim(50, 105)
plt.legend(loc='lower right')
for i in range(len(names)):
    plt.text(i - width/2, train_scores[i] + 1, f"{train_scores[i]:.1f}%", ha='center', fontsize=9, fontweight='bold')
    plt.text(i + width/2, test_scores[i] + 1, f"{test_scores[i]:.1f}%", ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/chart_11_model_comparison_bar.png', dpi=300)
plt.close()

# ROC Curves Plot
plt.figure(figsize=(8, 6))
for name, (fpr, tpr, roc_auc) in roc_data.items():
    plt.plot(fpr, tpr, label=f"{name} (AUC = {roc_auc:.2f})", linewidth=2)
plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing (AUC = 0.50)')
plt.title("ROC Curves Comparison Across Machine Learning Models", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("False Positive Rate", fontsize=11, fontweight='bold')
plt.ylabel("True Positive Rate", fontsize=11, fontweight='bold')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('assets/chart_12_roc_curves.png', dpi=300)
plt.close()

print("All figures and ML models executed successfully!")
