import dash
from dash import dcc, html, Input, Output, callback_context, State
import plotly.graph_objects as go
import pandas as pd

# 创建 Dash 应用
app = dash.Dash(__name__)

# 读取 Excel 数据
file_path = '/Users/shuting/Desktop/mda/group project/mda-app'
df = pd.read_excel("3_city_case_death.xlsx")

# 将 'Month' 列转换为日期格式
df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')

# 获取所有城市的列表
cities = df['City'].unique()

# 定义 Dash 应用布局
app.layout = html.Div(children=[
    html.H1(children='AED Mortality Rate Analysis by Different Years and Cities'),
    
    html.Div(
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df['Month'].dt.year.unique()],
            value=2022  # 设置初始值为2022
        ),
        style={'width': '200px', 'margin-top': '10px', 'margin-bottom': '20px'}  # 调整下拉菜单的宽度并靠左对齐
    ),

    html.Div(
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in cities],
            value='Brussels'  # 设置初始城市
        ),
        style={'width': '200px', 'margin-top': '10px', 'margin-bottom': '20px'}  # 调整下拉菜单的宽度并靠左对齐
    ),

    dcc.Graph(
        id='monthly-data-graph',
        style={'width': '80vw', 'height': '70vh'}  # 设置图表的宽度和高度
    )
])

# 设置回调函数，根据选择的年度更新图表数据
@app.callback(
    Output('monthly-data-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_figure(selected_year, selected_city):
    # 过滤出选择城市和选择年度的数据
    df_filtered = df[(df['City'] == selected_city) & (df['Month'].dt.year == selected_year)]

    # 获取选择年度和城市的月份，格式化为 2022-09 这样的格式
    months = df_filtered['Month'].dt.strftime('%Y-%m').tolist()
    total_cases = df_filtered['Total Cases'].tolist()
    deaths = df_filtered['Deaths'].tolist()
    death_rates = df_filtered['Death Rate (%)'].tolist()  # 假设 'Death Rate' 列包含百分比形式的死亡率

    # 创建柱状图
    fig = go.Figure()

    # 添加总病例的柱状图
    fig.add_trace(go.Bar(
        x=months, 
        y=total_cases,
        name='Total Cases',
    ))

    # 添加死亡人数的柱状图
    fig.add_trace(go.Bar(
        x=months, 
        y=deaths,
        name='Deaths',
    ))

    # 添加死亡率的折线图，使用副纵坐标轴
    fig.add_trace(go.Scatter(
        x=months,
        y=death_rates,
        name='Death Rate',
        yaxis='y2',
        mode='lines+markers'
    ))

    # 更新图表的布局，包括标题和轴标签
    fig.update_layout(
        title=f'Total Cases and Death Count in {selected_city} for {selected_year}',
        xaxis=dict(
            tickmode='array',
            tickvals=months , # 只显示月份标签
            tickformat='%Y-%m'
        ),
        yaxis=dict(
            title='Count',
        ),
        yaxis2=dict(
            title='Death Rate (%)',
            overlaying='y',
            side='right',
            tickformat='.1f'  # 确保副纵坐标轴显示正确的格式
        ),
        barmode='group',  # 将柱状图设置为分组显示
        legend=dict(
            x=1.05,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)