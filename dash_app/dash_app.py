import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import xml.etree.ElementTree as ET
import os
from pathlib import Path


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

BASE_DIR = Path(__file__).resolve().parent.parent


# Parse coverage.xml
coverage_source = os.path.join(BASE_DIR, 'coverage.xml')

tree = ET.parse(coverage_source)
root = tree.getroot()

# Extract data
data = []
for package in root.findall(".//package"):
    package_name = package.get('name')
    for class_ in package.findall(".//class"):
        class_name = class_.get('name')
        lines = class_.find('lines')
        total_lines = len(lines)
        if total_lines == 0:
            continue
        covered_lines = len([line for line in lines if line.get('hits') != '0'])
        coverage = (covered_lines / total_lines) * 100
        data.append({
            'Package': package_name,
            'Class': class_name,
            'Total Lines': total_lines,
            'Covered Lines': covered_lines,
            'Coverage': coverage
        })

df = pd.DataFrame(data)

# Create Dash app

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Test Coverage Dashboard"))),
    dbc.Row(dbc.Col(dcc.Graph(
        id='coverage-bar-chart',
        figure=px.bar(df, x='Class', y='Coverage', color='Package',
                      title="Test Coverage by Class",
                      labels={'Coverage': 'Coverage (%)', 'Class': 'Class'},
                      hover_data=['Total Lines', 'Covered Lines'])
    ))),
    dbc.Row(dbc.Col(dcc.Graph(
        id='coverage-pie-chart',
        figure=px.pie(df, names='Package', values='Coverage',
                      title="Coverage Distribution by Package",
                      labels={'Coverage': 'Coverage (%)'})
    )))
])


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
