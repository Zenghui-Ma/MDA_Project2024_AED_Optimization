import dash
from dash import dcc, html

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
                style={'fontSize': '24px', 'fontWeight': 'bold', 'lineHeight': '1.2'},
                children=title
            ),
            html.Div(
                style={'fontSize': '16px', 'position': 'absolute', 'right': '10px', 'lineHeight': '1.2'},
                children='Group of CHINA'
            )
        ]
    )


# Placeholder to push content below fixed header
placeholder = html.Div(style={'height': '60px'})
