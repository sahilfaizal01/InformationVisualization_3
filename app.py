# Importing the libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output

# Loading the cleaned data
df = pd.read_csv('cleaned_df.csv')

# Creating the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hours Worked Per Week vs Various Health and Lifestyle Factors"),
    html.H3("By Sahil Faizal - sf4140"),

    # Age range slider
    html.Div([
        html.Label("Select Age Range"),
        dcc.RangeSlider(
            id='age-slider',
            min=df['Age'].min(),
            max=df['Age'].max(),
            step=1,
            marks={i: str(i) for i in range(df['Age'].min(), df['Age'].max() + 1, 5)},
            value=[df['Age'].min(), df['Age'].max()]
        ),
    ]),

    # Dropdown for gender filter
    html.Div([
        html.Label("Select Gender"),
        dcc.Dropdown(
            id='gender-filter',
            options=[{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
            multi=True
        ),
    ]),

    # Dropdown for stress level filter
    html.Div([
        html.Label("Select Stress Level"),
        dcc.Dropdown(
            id='stress-filter',
            options=[{'label': stress_level, 'value': stress_level} for stress_level in df['Stress_Level'].unique()],
            multi=True
        ),
    ]),
    
    # Dropdown for work location filter
    html.Div([
        html.Label("Select Work Location"),
        dcc.Dropdown(
            id='location-filter',
            options=[{'label': location, 'value': location} for location in df['Work_Location'].unique()],
            multi=True
        ),
    ]),
    
    # Dropdown for industry filter
    html.Div([
        html.Label("Select Industry"),
        dcc.Dropdown(
            id='industry-filter',
            options=[{'label': industry, 'value': industry} for industry in df['Industry'].unique()],
            multi=True
        ),
    ]),

    # Dropdown for region filter
    html.Div([
        html.Label("Select Region"),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            multi=True
        ),
    ]),

    # Dropdown for job role filter
    html.Div([
        html.Label("Select Job Role"),
        dcc.Dropdown(
            id='job-role-filter',
            options=[{'label': job_role, 'value': job_role} for job_role in df['Job_Role'].unique()],
            multi=True
        ),
    ]),

    # Graph
    dcc.Graph(id='bar-plot')
])

# Defining the callback to update the graph based on filters
@app.callback(
    Output('bar-plot', 'figure'),
    Input('age-slider', 'value'),
    Input('gender-filter', 'value'),
    Input('stress-filter', 'value'),
    Input('location-filter', 'value'),
    Input('industry-filter', 'value'),
    Input('region-filter', 'value'),
    Input('job-role-filter', 'value')
)

def update_graph(selected_age_range, selected_genders, selected_stress_levels, selected_work_locations, selected_industry, selected_regions, selected_job_roles):
    # Filtering the data based on selected values
    filtered_df = df.copy()

    # Applying age range filter
    if selected_age_range:
        filtered_df = filtered_df[(filtered_df['Age'] >= selected_age_range[0]) & 
                                  (filtered_df['Age'] <= selected_age_range[1])]
    # Applying other filters
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    if selected_industry:
        filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industry)]
    if selected_work_locations:
        filtered_df = filtered_df[filtered_df['Work_Location'].isin(selected_work_locations)]
    if selected_stress_levels:
        filtered_df = filtered_df[filtered_df['Stress_Level'].isin(selected_stress_levels)]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_job_roles:
        filtered_df = filtered_df[filtered_df['Job_Role'].isin(selected_job_roles)]

    # Creating subplots for multiple bar charts
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=[
            "Work Hours vs Work Life Balance",
            "Work Hours vs Mental Health Condition",
            "Work Hours vs Sleep Quality",
            "Work Hours vs Physical Activity"
        ]
    )

    # Plotting each metric with x and y labels
    fig.add_trace(
        go.Bar(x=filtered_df['Work_Life_Balance_Rating'], y=filtered_df['Hours_Worked_Per_Week'], 
               name='Work Life Balance', marker_color='blue'),
        row=1, col=1
    )
    fig.update_xaxes(title_text="Work Life Balance Rating", row=1, col=1)
    fig.update_yaxes(title_text="Hours Worked Per Week", row=1, col=1)
    
    fig.add_trace(
        go.Bar(x=filtered_df['Mental_Health_Condition'], y=filtered_df['Hours_Worked_Per_Week'], 
               name='Mental Health Condition', marker_color='green'),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Mental Health Condition", row=1, col=2)
    fig.update_yaxes(title_text="Hours Worked Per Week", row=1, col=2)

    fig.add_trace(
        go.Bar(x=filtered_df['Sleep_Quality'], y=filtered_df['Hours_Worked_Per_Week'], 
               name='Sleep Quality', marker_color='orange'),
        row=1, col=3
    )
    fig.update_xaxes(title_text="Sleep Quality", row=1, col=3)
    fig.update_yaxes(title_text="Hours Worked Per Week", row=1, col=3)

    fig.add_trace(
        go.Bar(x=filtered_df['Physical_Activity'], y=filtered_df['Hours_Worked_Per_Week'], 
               name='Physical Activity', marker_color='purple'),
        row=1, col=4
    )
    fig.update_xaxes(title_text="Physical Activity", row=1, col=4)
    fig.update_yaxes(title_text="Hours Worked Per Week", row=1, col=4)

    fig.update_layout(
        height=600,
        showlegend=False,
        transition_duration=500
    )

    return fig

server = app.server

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
