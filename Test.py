import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_top_bar(title):
    return html.Div(
        style={
            'backgroundColor': '#1C4E80', 
            'color': 'white', 
            'padding': '10px 0', 
            'display': 'flex', 
            'justifyContent': 'center',
            'alignItems': 'center',
            'width': '100%',
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'zIndex': '1000',
            'margin': '0',
            'boxSizing': 'border-box'
        },
        children=[
            html.Div(
                children=[
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Home", href="http://localhost:8051"),
                            dbc.DropdownMenuItem("Map", href="http://localhost:8050"),
                            dbc.DropdownMenuItem("Page1", href="http://localhost:8053"),
                            dbc.DropdownMenuItem("Page2", href="http://localhost:8052")
                        ],
                        nav=True,
                        in_navbar=True,
                        label=html.Img(src='/assets/logo.png', height="30px", width="30px")
                    ),
                ],
                style={'position': 'absolute', 'left': '10px'}
            ),
            html.Div(
                style={'fontSize': '24px', 'fontWeight': 'bold'},
                children=title
            ),
            html.Div(
                style={'fontSize': '16px', 'position': 'absolute', 'right': '10px'},
                children='Group of CHINA'
            )
        ]
    )

# Placeholder to push content below fixed header
placeholder = html.Div(style={'height': '60px'})

app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '0', 'margin': '0', 'color': '#1C4E80'},
    children=[
    create_top_bar('AED Location Analytics'),
    placeholder,
    html.Div([
        html.H1("Project Introduction"),
        html.P("The visualization of this project consists of three parts:"),
        html.Ol([
            html.Li("Map visualization, including AED locations, hospitals, patient visualizations, and changes in patient survival rates with the addition of new AEDs."),
            html.Li("Monthly mortality rates, death rates for heart patients from June 2022 to May 2023."),
            html.Li("Annual mortality rates, summarizing cardiac patient mortality rates for different cities in 2022 and 2023.")
        ]),
        html.P("The data includes ambulance call data for cardiac patients located in the cities of Brussels, Antwerp, and Liege.")
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
