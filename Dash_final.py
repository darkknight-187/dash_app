import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df= pd.read_csv('./assets/final_alt_merge.csv')
###########################################################


# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])




app.layout = html.Div(dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Enrich Oil Company",
                className='text-center text-primary mb-4'),
        width=12)
    ),
    dbc.Row([
        dbc.Col([
                    html.Div("Select Well",style={'color': 'red', 'fontSize': 15}),

                     html.Br(),
                     dcc.Checklist(id='well_select', value=['Foraker_1H','Foraker_2H'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Well'].unique())],
                                  labelStyle = dict(display='block'),


                      ),
                     html.Br(),

                    html.Div("Proppant Range",style={'color': 'red', 'fontSize': 15}),
                    html.Br(),
                    dcc.RangeSlider(id='prop_range',
                    min=1000,
                    max=2500,
                    step=100,
                    value=[1000,2500],
                    marks={1000:'1000',2500:'2500'},
                    tooltip = { 'always_visible': True ,'placement':'bottom'},
                    updatemode ='drag'
                    ),
                    html.Br(),

                    html.Div("Fluid Range",style={'color': 'red', 'fontSize': 15}),
                    html.Br(),
                    dcc.RangeSlider(id='fluid_range',
                            min=1200,
                            max=3000,
                            step=100,
                            value=[1200, 3000],
                            marks={1200: '1200', 3000: '3000'},
                            tooltip={'always_visible': True, 'placement': 'bottom'},
                            updatemode='drag'
                            ),
                    html.Br(),

                    html.Div("Oil EUR Range",style={'color': 'red', 'fontSize': 15}),
                    html.Br(),
                    dcc.RangeSlider(id='oil_eur_range',
                            min=20,
                            max=200,
                            step=10,
                            value=[20, 200],
                            marks={20: '20', 200: '200'},
                            tooltip={'always_visible': True, 'placement': 'bottom'},
                            updatemode='drag'
                            ),


        ], width={'size':2, 'offset':0}),
        dbc.Col([
            html.Div("Oil Production", style={'color': 'black', 'fontSize': 15},className='text-left'),
            dcc.Graph(id='oil_line_grp', figure={}),
            html.Div("Water Production", style={'color': 'black', 'fontSize': 15},className='text-left'),
            dcc.Graph(id='water_line_grp', figure={}),
            ],width={'size':5, 'offset':0}),
        dbc.Col([
            html.Div("Prop vs EUR ", style={'color': 'black', 'fontSize': 15},className='text-left'),
            dcc.Graph(id='prop_eur'),
            html.Div("Fluid vs EUR", style={'color': 'black', 'fontSize': 15},className='text-left'),
            dcc.Graph(id='fluid_eur'),
            ],width={'size':4, 'offset':0})
    ])
], fluid=True)
)
# Callback section: connecting the components
# ************************************************************************

@app.callback(
    Output('oil_line_grp', 'figure'),
    Input(component_id='well_select', component_property='value'),
    Input(component_id='prop_range', component_property='value'),
    Input(component_id='fluid_range', component_property='value'),
    Input(component_id='oil_eur_range', component_property='value'),
    Input(component_id='prop_eur', component_property='selectedData'),
    Input(component_id='fluid_eur', component_property='selectedData')
)
def update_graph(well_sel,prop_sel,fluid_sel,oil_eur_sel,prop_slt,fluid_slt):
    if len(well_sel) > 0:
        dff=df.copy()
        # dff = dff[dff['Well'].isin(well_sel)]
        start_prop =prop_sel[0]
        end_prop =prop_sel[1]
        start_fluid = fluid_sel[0]
        end_fluid = fluid_sel[1]
        start_oil = oil_eur_sel[0]
        end_oil = oil_eur_sel[1]
        if prop_slt is not None:
            my_list = list(item['customdata'][0] for item in prop_slt['points'])
            my_list=list(set(my_list))
            well_sel =my_list
            dff = dff[dff['Well'].isin(well_sel)]
        else:
            dff = dff[dff['Well'].isin(well_sel)]

        if fluid_slt is not None:
            my_list = list(item['customdata'][0] for item in fluid_slt['points'])
            my_list=list(set(my_list))
            well_sel =my_list
            dff = dff[dff['Well'].isin(well_sel)]
        else:
            dff = dff[dff['Well'].isin(well_sel)]


        mask = (dff['PROP_FT'] > start_prop) & (dff['PROP_FT'] <= end_prop) & (dff['FLUID_FT'] > start_fluid) & (
                    dff['FLUID_FT'] <= end_fluid) & (dff['EUR_OIL'] > start_oil) & (dff['EUR_OIL'] <= end_oil)
        dff = dff.loc[mask]

        fig = px.line(dff, x="Months", y="Oil", color='Well',log_y=True)
        return fig
    elif len(well_sel) == 0:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('water_line_grp', 'figure'),
    Input(component_id='well_select', component_property='value'),
    Input(component_id='prop_range', component_property='value'),
    Input(component_id='fluid_range', component_property='value'),
    Input(component_id='oil_eur_range', component_property='value'),
    Input(component_id='prop_eur', component_property='selectedData'),
    Input(component_id='fluid_eur', component_property='selectedData')
)
def update_graph(well_sel,prop_sel,fluid_sel,oil_eur_sel,prop_slt,fluid_slt):
    if len(well_sel) > 0:
        dff = df.copy()
        start_prop = prop_sel[0]
        end_prop = prop_sel[1]
        start_fluid = fluid_sel[0]
        end_fluid = fluid_sel[1]
        start_oil = oil_eur_sel[0]
        end_oil = oil_eur_sel[1]
        if prop_slt is not None:
            my_list = list(item['customdata'][0] for item in prop_slt['points'])
            my_list=list(set(my_list))
            well_sel =my_list
            dff = dff[dff['Well'].isin(well_sel)]
        else:
            dff = dff[dff['Well'].isin(well_sel)]

        if fluid_slt is not None:
            my_list = list(item['customdata'][0] for item in fluid_slt['points'])
            my_list=list(set(my_list))
            well_sel =my_list
            dff = dff[dff['Well'].isin(well_sel)]
        else:
            dff = dff[dff['Well'].isin(well_sel)]

        mask = (dff['PROP_FT'] > start_prop) & (dff['PROP_FT'] <= end_prop) & (dff['FLUID_FT'] > start_fluid) & (
                dff['FLUID_FT'] <= end_fluid) & (dff['EUR_OIL'] > start_oil) & (dff['EUR_OIL'] <= end_oil)
        dff = dff.loc[mask]
        fig = px.line(dff, x="Months", y="Water", color='Well',log_y=True)
        # fig.update_layout(yaxis_range=[0, max_wat])
        return fig
    elif len(well_sel) == 0:
        raise dash.exceptions.PreventUpdate


@app.callback(
    Output('prop_eur', 'figure'),
    Input(component_id='well_select', component_property='value'),
    Input(component_id='prop_range', component_property='value'),
    Input(component_id='fluid_range', component_property='value'),
    Input(component_id='oil_eur_range', component_property='value')
)
def update_graph(well_sel,prop_sel,fluid_sel,oil_eur_sel):
    if len(well_sel) > 0:
        dff = df.copy()
        dff = dff[dff['Well'].isin(well_sel)]
        start_prop = prop_sel[0]
        end_prop = prop_sel[1]
        start_fluid = fluid_sel[0]
        end_fluid = fluid_sel[1]
        start_oil = oil_eur_sel[0]
        end_oil = oil_eur_sel[1]
        mask = (dff['PROP_FT'] > start_prop) & (dff['PROP_FT'] <= end_prop) & (dff['FLUID_FT'] > start_fluid) & (
                dff['FLUID_FT'] <= end_fluid) & (dff['EUR_OIL'] > start_oil) & (dff['EUR_OIL'] <= end_oil)
        dff = dff.loc[mask]

        fig = px.scatter(dff, x="PROP_FT", y="EUR_OIL", color='Well',log_y=True,hover_name="Well",custom_data=['Well'])
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=2,
                                                color='DarkSlateGrey')))
        fig.update_layout(transition_duration=500)
        return fig
    elif len(well_sel) == 0:
        raise dash.exceptions.PreventUpdate


@app.callback(
    Output('fluid_eur', 'figure'),
    Input(component_id='well_select', component_property='value'),
    Input(component_id='prop_range', component_property='value'),
    Input(component_id='fluid_range', component_property='value'),
    Input(component_id='oil_eur_range', component_property='value')
)
def update_graph(well_sel,prop_sel,fluid_sel,oil_eur_sel):
    if len(well_sel) > 0:
        dff = df.copy()
        dff = dff[dff['Well'].isin(well_sel)]
        start_prop = prop_sel[0]
        end_prop = prop_sel[1]
        start_fluid = fluid_sel[0]
        end_fluid = fluid_sel[1]
        start_oil = oil_eur_sel[0]
        end_oil = oil_eur_sel[1]
        mask = (dff['PROP_FT'] > start_prop) & (dff['PROP_FT'] <= end_prop) & (dff['FLUID_FT'] > start_fluid) & (
                dff['FLUID_FT'] <= end_fluid) & (dff['EUR_OIL'] > start_oil) & (dff['EUR_OIL'] <= end_oil)
        dff = dff.loc[mask]
        fig = px.scatter(dff, x="FLUID_FT", y="EUR_OIL", color='Well',log_y=True,custom_data=['Well'])
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=2,
                                                color='DarkSlateGrey')),
                          selector=dict(mode='markers'))
        # fig.update_layout(yaxis_range=[0, max_wat])
        return fig
    elif len(well_sel) == 0:
        raise dash.exceptions.PreventUpdate




if __name__=='__main__':
    app.run_server(debug=True, port=8000)

