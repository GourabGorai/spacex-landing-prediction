import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('assets', exist_ok=True)

# 1. API Flowchart Diagram
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# Title
ax.text(5, 4.6, "SpaceX REST API Data Collection Methodology", fontsize=13, fontweight='bold', ha='center', color='#0F172A')

boxes = [
    ("1. HTTP GET Request\nhttps://api.spacexdata.com/v4/launches/past", (0.5, 2.5), "#3B82F6"),
    ("2. JSON Response Parsing\nExtract core, payload,\nrocket, & launchsite IDs", (2.8, 2.5), "#6366F1"),
    ("3. Relational API Queries\nFetch Payload Mass, Orbit,\nLanding Pad, & Booster Serial", (5.1, 2.5), "#8B5CF6"),
    ("4. Data Cleaning & Encoding\nFilter Falcon 9, impute payload,\ncreate outcome binary target (Class)", (7.4, 2.5), "#10B981")
]

for title, (x, y), color in boxes:
    rect = patches.FancyBboxPatch((x, y-0.6), 2.1, 1.2, boxstyle="round,pad=0.1", ec=color, fc=color, alpha=0.15, lw=2)
    ax.add_patch(rect)
    ax.text(x + 1.05, y, title, fontsize=9, fontweight='bold', ha='center', va='center', color='#1E293B')

# Add arrows
for i in range(3):
    ax.annotate('', xy=(boxes[i+1][1][0] - 0.05, 2.5), xytext=(boxes[i][1][0] + 2.15, 2.5),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=2.5))

plt.tight_layout()
plt.savefig('assets/flowchart_api.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Web Scraping Flowchart Diagram
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

ax.text(5, 4.6, "Wikipedia Web Scraping Methodology (BeautifulSoup)", fontsize=13, fontweight='bold', ha='center', color='#0F172A')

boxes_ws = [
    ("1. Request Wikipedia Page\nList of Falcon 9 launches\nvia requests.get()", (0.5, 2.5), "#0284C7"),
    ("2. HTML DOM Parsing\nBeautifulSoup(response.text,\n'html.parser')", (2.8, 2.5), "#0D9488"),
    ("3. Table Extraction\nExtract launch #, date,\nbooster, payload, orbit, outcome", (5.1, 2.5), "#D97706"),
    ("4. DataFrame Structuring\nClean text, strip footnotes,\nconvert types & export CSV", (7.4, 2.5), "#059669")
]

for title, (x, y), color in boxes_ws:
    rect = patches.FancyBboxPatch((x, y-0.6), 2.1, 1.2, boxstyle="round,pad=0.1", ec=color, fc=color, alpha=0.15, lw=2)
    ax.add_patch(rect)
    ax.text(x + 1.05, y, title, fontsize=9, fontweight='bold', ha='center', va='center', color='#1E293B')

for i in range(3):
    ax.annotate('', xy=(boxes_ws[i+1][1][0] - 0.05, 2.5), xytext=(boxes_ws[i][1][0] + 2.15, 2.5),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=2.5))

plt.tight_layout()
plt.savefig('assets/flowchart_scraping.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. SQL Results Summary Table Graphic
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.axis('off')
ax.text(0.5, 0.95, "Key Exploratory SQL Data Analysis Results (SPACEXTBL)", fontsize=13, fontweight='bold', ha='center', color='#0F172A')

table_data = [
    ["Query Category", "SQL Function / Logic", "Key Result / Insight"],
    ["Launch Sites", "SELECT DISTINCT Launch_Site", "CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40"],
    ["NASA Payloads", "SUM(PAYLOAD_MASS__KG_) WHERE NASA", "Total Payload: 45,596 kg carried for NASA CRS missions"],
    ["F9 v1.1 Avg", "AVG(PAYLOAD_MASS__KG_) WHERE F9 v1.1", "Average Payload Mass: 2,928.4 kg"],
    ["First Landing", "MIN(Date) WHERE Success (ground pad)", "First successful ground landing achieved on 2015-12-22"],
    ["Max Payload", "MAX(PAYLOAD_MASS__KG_)", "Maximum Payload: 15,600 kg (achieved by B1048, B1049, etc.)"],
    ["Outcomes 10-17", "GROUP BY Landing_Outcome 2010-2017", "Success (drone ship): 12 | No attempt: 10 | Uncontrolled: 2"]
]

table = ax.table(cellText=table_data, loc='center', cellLoc='left', colWidths=[0.22, 0.40, 0.38])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.1, 1.6)

for (r, c), cell in table.get_celld().items():
    cell.set_linewidth(0.5)
    if r == 0:
        cell.set_facecolor('#1E293B')
        cell.get_text().set_color('white')
        cell.get_text().set_weight('bold')
    else:
        cell.set_facecolor('#F8FAFC' if r % 2 == 0 else '#FFFFFF')

plt.tight_layout()
plt.savefig('assets/chart_6_sql_results_table.png', dpi=300, bbox_inches='tight')
plt.close()

print("Diagrams generated successfully!")
