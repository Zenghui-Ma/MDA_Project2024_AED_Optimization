import dash
from dash import dcc, html
from layout import create_top_bar, placeholder

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义应用的布局
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '0', 'margin': '0'},
    children=[
        # Top blue bar
        create_top_bar('AED Location Analytics'),
        placeholder,

        # Main content divided into four parts
        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gridTemplateRows': '1fr 1fr', 'gap': '20px', 'padding': '20px'},
            children=[
                html.Div(
                    style={'border': '1px solid #ccc', 'padding': '10px', 'height': '400px', 'overflow': 'auto'},
                    children=[
                        html.H2('Text Area'),
                        html.P('This is the area for text input.')
                    ]
                ),
                html.Div(
                    style={'border': '1px solid #ccc', 'textAlign': 'center', 'height': '400px'},
                    children=[
                        html.A(
                            href='http://localhost:8050',
                            children=[
                                html.Img(src='/assets/Main_page_Maps.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                                html.P('Pages')
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'border': '1px solid #ccc', 'textAlign': 'center', 'height': '400px'},
                    children=[
                        html.A(
                            href='http://localhost:8053',
                            children=[
                                html.Img(src='/assets/page1.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                                html.P('Visitors')
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'border': '1px solid #ccc', 'textAlign': 'center', 'height': '400px'},
                    children=[
                        html.A(
                            href='http://localhost:8052',
                            children=[
                                html.Img(src='/assets/page2.png', style={'width': '100%', 'height': '100%', 'objectFit': 'cover'}),
                                html.P('Pages/Visitors')
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# 运行服务器并指定端口号，例如：8051
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
