# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 22:19:55 2020

@author: tallu
"""

#importing all required libraries

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import webbrowser as wb
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import time


app = dash.Dash()  #global variable of class Dash()

#defining global dictionary colors
colors = {
            'background1':'#000000',
            'text1':'#ffffff ',
            'background2':'#111111',
            'text2':'#00ffff',
            'background3':'#ffffff',
            'background4':'#808080'
            }

def load_data():    #function to load all the data 
    
    dataset = 'global_terror1.csv'  
    
    pd.options.mode.chained_assignment = None

    
    global df 
    df = pd.read_csv(dataset)
      
    global year_list , year_dict
    year_list = sorted(df['iyear'].unique().tolist())
    year_dict = {str(year):str(year)  for year in year_list}  
    
    global month , month_dict , day_dict 
    month= {'January':1,
                 'February':2,
                 'March':3,
                 'April':4,
                 'May':5,
                 'June':6,
                 'July':7,
                 'August':8,
                 'September':9,
                 'October':10,
                 'November':11,
                 'December':12
                    }
    month_dict= [{'label':key,'value':values  } for key,values in month.items()]
        
    day_dict= [{'label':d,'value':d } for d in range(1,32)]
        
    global  region_dict  , country_dict , state_dict , city_dict
    
    region_dict= [{'label':str(region),'value':str(region)  }for region in sorted(df['region_txt'].unique().tolist())]
   
    country_dict = df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()
    #country_dict = [{'label':str(i),'value':str(i)}  for i in sorted(df['country_txt'].unique().tolist()) ]    
    
    state_dict = df.groupby('country_txt')['provstate'].unique().apply(list).to_dict()
    #state_dict= [{'label':state,'value':state  }for state in sorted(df['provstate'].astype(str).unique().tolist())]
         
    city_dict = df.groupby('provstate')['city'].unique().apply(list).to_dict() 
    #city_dict= [{'label':city,'value':city }for city in sorted(df['city'].astype(str).unique().tolist())]    
    
    global attack_dict 
    attack_dict = [{'label':attack,'value':attack } for attack in sorted(df['attacktype1_txt'].unique().tolist()) ]
    
    global chart_dict
    chart_dict =        {    "Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
    
    chart_dict = [{'label':keys , 'value':value}    for keys,value in chart_dict.items()]

    
    
    
    
    
def open_browser():     #function to open web browser
    
    wb.open_new('http://127.0.0.1:8050/')

    

def ui():       #function to design all the UI components 
    
    layout = html.Div(style = {'backgroundColor':colors['background4'] 

    },
                      
    children =
    [
        html.H1(id='Heading',
                children='Terrorism Analysis',
                style={'textAlign':'center','color':colors['text1']}
                ),
        
                
        dcc.Tabs(id='Tabs',
                 value='tab-1',
                 children=[dcc.Tab(label='Map Tool',
                                   id = 'Map Tool',
                                   value = 'Tab-1',
                                   children = [dcc.Tabs(id='Subtabs-1',
                                                        value = 'Tab-1',
                                                        children = [dcc.Tab(label='World Map Tool',
                                                                            id = 'World',
                                                                            value = 'Tab-1',
                                                                            children = [html.Div([  
                                                                                                   html.H2('Select the filters below',
                                                                                                           style={'textAlign':'center',
                                                                                                                  'color':colors['text1']}
                                                                                                           ),
                                                                                                  
                                                                                                   html.Hr(),
                                                                                                   
                                                                                                   html.Div([
                                                                                                       
                                                                                                       html.Div(style={'width':'50%'},
                                                                                                                children=
                                                                                                                       [
                                                                                                                       html.H3('Time filter',
                                                                                                                                   style={'textAlign':'center',
                                                                                                                                          'color':colors['text1'],
                                                                                                                                          'margin-right':'2em'}
                                                                                                                                   ),
                                                                                                                       html.Div(style={'margin-left':'170px'},
                                                                                                                                children=
                                                                                                                                [
                                                                                                                                   dcc.Dropdown(id='Dropdown_1',
                                                                                                                                                 options=month_dict,
                                                                                                                                                 placeholder='Select month...',
                                                                                                                                                 multi=True,
                                                                                                                                                 style=dict(width='80%',
                                                                                                                                                            verticalAlign='middle')
                                                                                                                                                 ),
                                                                                                                                    
                                                                                                                                    dcc.Dropdown(id='Dropdown_2',
                                                                                                                                                 options=day_dict,
                                                                                                                                                 placeholder='Select date...',
                                                                                                                                                 multi=True,
                                                                                                                                                 style=dict(width='80%',
                                                                                                                                                            verticalAlign='middle')
                                                                                                                                                 )
                                                                                                                                    ])
                                                                                                                        ]
                                                                                                           ),
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    html.Div(style={'width':'50%',
                                                                                                                    },
                                                                                                             children=
                                                                                                            [
    
                                                                                                            html.H3('Location filter',
                                                                                                                    style={'textAlign':'center',
                                                                                                                           'color':colors['text1'],
                                                                                                                           'margin-right':'2em'}
                                                                                                                    ),
                                                                                                            
                                                                                                            
                                                                                                            html.Div(style={'margin-left':'170px'},
                                                                                                                     children=
                                                                                                                [
                                                                                                                        dcc.Dropdown(id='Dropdown_3',
                                                                                                                                     options=region_dict,
                                                                                                                                     placeholder='Select region...',
                                                                                                                                     multi=True,
                                                                                                                                     style=dict(width='80%',
                                                                                                                                                verticalAlign='middle')
                                                                                                                                     ),
                                                                                                                          
                                                                                                                        dcc.Dropdown(id='Dropdown_4',
                                                                                                                                     options = country_dict,
                                                                                                                                     placeholder='Select country...',
                                                                                                                                     multi=True,
                                                                                                                                     style=dict(width='80%',
                                                                                                                                                verticalAlign='middle')
                                                                                                                                     ),
                                                                                                                        
                                                                                                                           
                                                                                                                        dcc.Dropdown(id='Dropdown_5',
                                                                                                                                     options=state_dict,
                                                                                                                                     placeholder='Select state or province...',
                                                                                                                                     multi=True,
                                                                                                                                     style=dict(width='80%',
                                                                                                                                                verticalAlign='middle')
                                                                                                                                     ),
                                                                                                                          
                                                                                                                              
                                                                                                                        dcc.Dropdown(id='Dropdown_6',
                                                                                                                                     options=city_dict,
                                                                                                                                     placeholder='Select city...',
                                                                                                                                     multi=True,
                                                                                                                                     style=dict(width='80%',
                                                                                                                                                verticalAlign='middle')
                                                                                                                                     ),
                                                                                                                        
                                                                                                                            
                                                                                                                        dcc.Dropdown(id='Dropdown_7',
                                                                                                                                     options=attack_dict,
                                                                                                                                     placeholder='Select attack type...',
                                                                                                                                     multi=True,
                                                                                                                                     style=dict(width='80%',
                                                                                                                                                verticalAlign='middle')
                                                                                                                                     )
                                                                                                                        ])
                                                                                                            
                                                                                                            ]
                                                                                                        ),
                                                                                                    ],
                                                                                                       style=dict(display='flex')
                                                                                                       
                                                                                                      
                                                                                                       
                                                                                                       ),
                                                                                                    
                                                                                                    html.Br(),        
                                                                                                    
                                                                                                    html.Hr(),
                                                                                                    
                                                                                                    html.H3('Year Range filter',
                                                                                                            style={'color':colors['text1'],
                                                                                                                   'textAlign':'center'}
                                                                                                            ),
                                                                                                    html.Div(style={'backgroundColor':colors['background3']},
                                                                                                             children=
                                                                                                        
                                                                                                        [       html.Br(),
                                                                                                         
                                                                                                                dcc.RangeSlider(id='year_slider',
                                                                                                                       min=min(year_list),
                                                                                                                       max=max(year_list),
                                                                                                                       value=[min(year_list),max(year_list)],   #default value of slider
                                                                                                                       marks=year_dict, #slider interval
                                                                                                                       step = None  
                                                                                                                       )
                                                                                                            ]
                                                                                                           
                                                                                                           ),
                                                                                                        
                                                                                                    dcc.Loading(id='Loading_1',
                                                                                                                children=html.Div(id='loading_1')) 
                                                                                                    
                                                                                                    
                                                                                                    ]
                                                                                
                                                                                                    )
                                                                                ]
                                                                            ),
                                                            
                                                                    dcc.Tab(label='India Map Tool',
                                                                            id = 'India',
                                                                            value = 'Tab-2',
                                                                            children = [html.Div([
                                                                                                   html.H2('Select the filters below',
                                                                                                           style={'textAlign':'center',
                                                                                                                  'color':colors['text1']}
                                                                                                           ),
                                                                                                  
                                                                                                   html.Hr(),
                                                                                                   
                                                                                                   html.Div([
                                                                                                       
                                                                                                       html.Div(style={'width':'50%'},
                                                                                                                children=
                                                                                                                       [
                                                                                                                       html.H3('Time filter',
                                                                                                                                   style={'textAlign':'center',
                                                                                                                                          'color':colors['text1'],
                                                                                                                                          'margin-right':'2em'}
                                                                                                                                   ), 
                                                                                                                       
                                                                                                                       html.Div(style={'margin-left':'170px'},
                                                                                                                           children=
                                                                                                                           [
                                                                                                                                   dcc.Dropdown(id='Dropdown_a',
                                                                                                                                                 options=month_dict,
                                                                                                                                                 placeholder='Select month...',
                                                                                                                                                 multi=True,
                                                                                                                                                 style=dict(width='80%',
                                                                                                                                                            verticalAlign='middle')
                                                                                                                                                 ),
                                                                                                                                    
                                                                                                                                    dcc.Dropdown(id='Dropdown_b',
                                                                                                                                                 options=day_dict,
                                                                                                                                                 placeholder='Select date...',
                                                                                                                                                 multi=True,
                                                                                                                                                 style=dict(width='80%',
                                                                                                                                                            verticalAlign='middle',
                                                                                                                                                            )
                                                                                                                             
                                                                                                                                                    )
                                                                                                                                    ])
                                                                                                                    ]
                                                                                                                 ),
                                                                                                    
                                                                                                        
                                                                                                    html.Div(style={'width':'50%',
                                                                                                                    },
                                                                                                             children=
                                                                                                            [
    
                                                                                                            html.H3('Location filter',
                                                                                                                    style={'textAlign':'center',
                                                                                                                           'color':colors['text1'],
                                                                                                                           'margin-right':'2em'}
                                                                                                                    ),
                                                                                                        
                                                                                                                
                                                                                                                html.Div(style={'margin-left':'170px'},
                                                                                                                    children=
                                                                                                                    [
                                                                                                                            dcc.Dropdown(id='Dropdown_c',
                                                                                                                                         options=region_dict,
                                                                                                                                         multi=True,
                                                                                                                                         value=['South Asia'],
                                                                                                                                         clearable=False,
                                                                                                                                         style=dict(width='80%',
                                                                                                                                                    verticalAlign='middle')
                                                                                                                                         ),
                                                                                                                              
                                                                                                                            dcc.Dropdown(id='Dropdown_d',
                                                                                                                                         options = country_dict,
                                                                                                                                         multi=True,
                                                                                                                                         value=['India'],
                                                                                                                                         clearable=False,
                                                                                                                                         style=dict(width='80%',
                                                                                                                                                    verticalAlign='middle')
                                                                                                                                         ),
                                                                                                                            
                                                                                                                               
                                                                                                                            dcc.Dropdown(id='Dropdown_e',
                                                                                                                                         options=state_dict,
                                                                                                                                         placeholder='Select state or province...',
                                                                                                                                         multi=True,
                                                                                                                                         style=dict(width='80%',
                                                                                                                                                    verticalAlign='middle')
                                                                                                                                         ),
                                                                                                                              
                                                                                                                                  
                                                                                                                            dcc.Dropdown(id='Dropdown_f',
                                                                                                                                         options=city_dict,
                                                                                                                                         placeholder='Select city...',
                                                                                                                                         multi=True,
                                                                                                                                         style=dict(width='80%',
                                                                                                                                                    verticalAlign='middle')
                                                                                                                                         ),
                                                                                                                            
                                                                                                                                
                                                                                                                            dcc.Dropdown(id='Dropdown_g',
                                                                                                                                         options=attack_dict,
                                                                                                                                         placeholder='Select attack type...',
                                                                                                                                         multi=True,
                                                                                                                                         style=dict(width='80%',
                                                                                                                                                    verticalAlign='middle')
                                                                                                                                         )
                                                                                                                            ])
                                                                                                                ]
                                                                                                                 )
                                                                                                                             ],
                                                                                                       style=dict(display='flex')
                                                                                                                 
                                                                                                                 ),
                                                                                                    
                                                                                                    html.Br(),        
                                                                                                    
                                                                                                    html.Hr(),
                                                                                                    
                                                                                                    html.H3('Year Range filter',
                                                                                                            style={'textAlign':'center',
                                                                                                                   'color':colors['text1']
                                                                                                                   }
                                                                                                            ),
                                                                                                    
                                                                                                    html.Div(style={'backgroundColor':colors['background3']},
                                                                                                        children=
                                                                                                        [
                                                                                                            html.Br(),
                                                                                                            
                                                                                                            dcc.RangeSlider(id='year_slider1',
                                                                                                                            min=min(year_list),
                                                                                                                            max=max(year_list),
                                                                                                                            value=[min(year_list),max(year_list)],   #default value of slider
                                                                                                                            marks=year_dict,
                                                                                                                            step = None , #slider interval
                                                                                                                   
                                                                                                                   )
                                                                                                            ]),
                                                                                                        
                                                                                                    dcc.Loading(id='Loading_2',
                                                                                                                children=html.Div(id='loading_2')) ]
                                                                                
                                                                                                    )]
                                                                            
                                                                            )
                                                            
                                                                ]
                                                
                                                       )
                                               ]
                                       ),
                           
                           dcc.Tab(label='Chart Tool',
                                   id = 'Chart Tool',
                                   value = 'Tab-3',
                                   children = [dcc.Tabs(id='Subtabs-2',
                                                        value = 'Chart',
                                                        children = [dcc.Tab(label='World Chart Tool',
                                                                            id = 'WorldC',
                                                                            value = 'Tab-3',
                                                                            children = [html.Div([  
                                                                                                     html.H2('Select the filters below',
                                                                                                              style={'textAlign':'center',
                                                                                                              'color':colors['text1']}
                                                                                                            ),
                                                                                                              
                                                                                                                html.Hr(),
                                                                                                                html.Div([
                                                                                                                            html.Div(style={'width':'50%'},
                                                                                                                                children=[
                                                                                                                                
                                                                                                                                            html.H3('Parametric filter',
                                                                                                                                                    style={'textAlign':'center',
                                                                                                                                                           'color':colors['text1'],
                                                                                                                                                           'margin-right':'2em'}
                                                                                                                                                    ),
                                                                                                                                            html.Div(style={'margin-left':'170px'},
                                                                                                                                                children=
                                                                                                                                                [
                                                                                                                                                        dcc.Dropdown(id='Dropdown_wc',
                                                                                                                                                                   options=chart_dict,
                                                                                                                                                                   placeholder='Select an option...',
                                                                                                                                                                   value = 'region_txt',
                                                                                                                                                                   style=dict(width='80%',
                                                                                                                                                                                verticalAlign='middle')
                                                                                                                                                                   )]
                                                                                                                                                      )
                                                                                                                            ]
                                                                                                                                       ),
                                                                                                                html.Div(style={'width':'50%'},
                                                                                                                    children=[
                                                                                                                        
                                                                                                                html.H3('Filter Specific Values',
                                                                                                                        style={'textAlign':'center',
                                                                                                                               'color':colors['text1'],
                                                                                                                               'margin-right':'2em'}
                                                                                                                        ),
                                                                                                                
                                                                                                                html.Div(style={'margin-left':'275px'},
                                                                                                                    children=
                                                                                                                    [
                                                                                                                dcc.Input(id='search',
                                                                                                                          placeholder='Search filter')
                                                                                                                
                                                                                                                ])
                                                                                                                ])
                                                                                                                ],
                                                                                                                    style=dict(display='flex'))
                                                                                                    ]
                                                                                ),
                                                                                                    
                                                                                html.Br(),        
                                                                                                    
                                                                                html.Hr(),
                                                                                                    
                                                                                html.H3('Year Range filter',
                                                                                        style={'textAlign':'center',
                                                                                               'color':colors['text1']
                                                                                               }
                                                                                        ),
                                                                                                    
                                                                                html.Div(style={'backgroundColor':colors['background3']},
                                                                                         children=
                                                                                         [
                                                                                             html.Br(),

                                                                                             dcc.RangeSlider(id='year_slider1c',
                                                                                                            min=min(year_list),
                                                                                                            max=max(year_list),
                                                                                                            value=[min(year_list),max(year_list)],   #default value of slider
                                                                                                            marks=year_dict ,
                                                                                                            step = None #slider interval
                                                                                                          )  
                                                                                                        ]
                                                                                                        ),

                                                                                        dcc.Loading(id='wc'
                                                                                        )
                                                                                        ]
                                                                            ),
                                                                    
                                                                    dcc.Tab(label='India Chart Tool',
                                                                            id = 'IndiaC',
                                                                            value = 'Tab-4',
                                                                            children = [html.Div([  
                                                                                                     html.H2('Select the filters below',
                                                                                                              style={'textAlign':'center',
                                                                                                              'color':colors['text1']}
                                                                                                            ),
                                                                                                              
                                                                                                                html.Hr(),
                                                                                                                html.Div([
                                                                                                                            html.Div(style={'width':'50%'},
                                                                                                                                children=[
                                                                                                                                
                                                                                                                                            html.H3('Parametric filter',
                                                                                                                                                    style={'textAlign':'center',
                                                                                                                                                           'color':colors['text1'],
                                                                                                                                                           'margin-right':'2em'}
                                                                                                                                                    ),
                                                                                                                                            html.Div(style={'margin-left':'170px'},
                                                                                                                                                children=
                                                                                                                                                [
                                                                                                                                                        dcc.Dropdown(id='Dropdown_ic',
                                                                                                                                                                   options=chart_dict,
                                                                                                                                                                   placeholder='Select an option...',
                                                                                                                                                                   value = 'region_txt',
                                                                                                                                                                   style=dict(width='80%',
                                                                                                                                                                                verticalAlign='middle')
                                                                                                                                                                   )]
                                                                                                                                                      )
                                                                                                                            ]
                                                                                                                                       ),
                                                                                                                html.Div(style={'width':'50%'},
                                                                                                                    children=[
                                                                                                                        
                                                                                                                html.H3('Filter Specific Values',
                                                                                                                        style={'textAlign':'center',
                                                                                                                               'color':colors['text1'],
                                                                                                                               'margin-right':'2em'}
                                                                                                                        ),
                                                                                                                
                                                                                                                html.Div(style={'margin-left':'275px'},
                                                                                                                    children=
                                                                                                                    [
                                                                                                                dcc.Input(id='search_1',
                                                                                                                          placeholder='Search filter')
                                                                                                                
                                                                                                                ])
                                                                                                                ])
                                                                                                                ],
                                                                                                                    style=dict(display='flex'))
                                                                                                    ]
                                                                                ),
                                                                                                    
                                                                                html.Br(),        
                                                                                                    
                                                                                html.Hr(),
                                                                                                    
                                                                                html.H3('Year Range filter',
                                                                                        style={'textAlign':'center',
                                                                                               'color':colors['text1']
                                                                                               }
                                                                                        ),
                                                                                                    
                                                                                html.Div(style={'backgroundColor':colors['background3']},
                                                                                         children=
                                                                                         [
                                                                                             html.Br(),

                                                                                             dcc.RangeSlider(id='year_slider2c',
                                                                                                            min=min(year_list),
                                                                                                            max=max(year_list),
                                                                                                            value=[min(year_list),max(year_list)],   #default value of slider
                                                                                                            marks=year_dict ,
                                                                                                            step = None #slider interval
                                                                                                          )  
                                                                                                        ]
                                                                                                        ),

                                                                                       dcc.Loading(id='ic'
                                                                                                ) 
                                                                                                ]
                                                                                                )
                                                                    
                                                                    ]
                                                        
                                       
                                                           )
                                               ]
                                   
                                   )
                             
                           
                           
                           
                           
                           ])
        
        
        
        
        
        
        
       ])
    
    
    return layout
    
    
#For World map 
#callback for map 
@app.callback(
        dash.dependencies.Output('loading_1', 'children'),
        
        [dash.dependencies.Input('Dropdown_1', 'value'),
         dash.dependencies.Input('Dropdown_2', 'value'),
         dash.dependencies.Input('Dropdown_3', 'value'),
         dash.dependencies.Input('Dropdown_4', 'value'),
         dash.dependencies.Input('Dropdown_5', 'value'),
         dash.dependencies.Input('Dropdown_6', 'value'),
         dash.dependencies.Input('Dropdown_7', 'value'),         
         dash.dependencies.Input('year_slider','value')
         ]
    )
    

def update_ui(dd1,dd2,dd3,dd4,dd5,dd6,dd7,slider):
    #best practices to print datatype and values of paramters passed
    print('\nDatatype of dd1:',type(dd1))
    print('Value of dd1:',str(dd1))
    
    print('\nDatatype of dd2:',type(dd2))
    print('Value of dd2:',str(dd2))
    
    print('\nDatatype of dd3:',type(dd3))
    print('Value of dd3:',str(dd3))
    
    print('\nDatatype of dd4:',type(dd4))
    print('Value of dd4:',str(dd4))
    
    print('\nDatatype of dd5:',type(dd5))
    print('Value of dd5:',str(dd5))
    
    print('\nDatatype of dd6:',type(dd6))
    print('Value of dd6:',str(dd6))
    
    print('\nDatatype of dd7:',type(dd7))
    print('Value of dd7:',str(dd7))
       
    print('\nDatatype of slider:',type(slider))
    print('Value of slider:',str(slider))
    
    
    #year_filter
    year_range = range (slider[0],slider[1]+1)
   
    new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

    new_df = df[df['iyear'].isin(year_range)]
    
    
    
    #blank figure
    fig = go.Figure()
    
    
    #month and day filter
    if  dd1 == [] or dd1 is None :
        
        pass
        
    
    else:
        
            if dd2 == [] or dd2 is None :
           
                new_df = new_df[new_df['imonth'].isin(dd1)]
                
            else:
                
                new_df = new_df[(new_df['imonth'].isin(dd1)) & 
                             (new_df['iday'].isin(dd2))
                             ]
    
        
    #region, country, state and city filter
    if dd3 == [] or dd3 is None:
        
        pass
    
    else:
        
        if dd4 == [] or dd4 is None:
            
            new_df = new_df[new_df['region_txt'].isin(dd3)]
            
        else:
            
            if dd5 == [] or dd5 is None:
                
                new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                (new_df['country_txt'].isin(dd4))
                                ]
            
            else:
                
                if dd6 == [] or dd6 is None:
            
                    new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                    (new_df['country_txt'].isin(dd4)) &
                                    (new_df['provstate'].isin(dd5))
                                    ]
            
                else:
                   
                    new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                    (new_df['country_txt'].isin(dd4)) &
                                    (new_df['provstate'].isin(dd5)) &
                                    (new_df['city'].isin(dd6))
                                    ]
            
            
    #attack type filter
    if dd7 == [] or dd7 is None:
        
        pass
    
    else:
        
        new_df = new_df[new_df['attacktype1_txt'].isin(dd7)]
        
         
    #creating map   
    fig = px.scatter_mapbox(new_df,
                              lat='latitude',
                              lon='longitude',
                              hover_data=['iyear','region_txt','country_txt','provstate','city','nkill'],
                              color='attacktype1_txt',
                              labels=attack_dict,
                              height=800,
                              zoom=1
                              )
    
    fig.update_layout(mapbox_style='carto-darkmatter',
                          legend=dict(  orientation = 'h',
                                        x=0,
                                        y=0,
                                        
                                        title_font_family="Times New Roman",
                                        font=dict(
                                            family="Courier",
                                            size=13.55,
                                            color=colors['text1']
                                            
                                        ),
                                        bgcolor="black",
                                        bordercolor="White",
                                        borderwidth=1
                                    ),
                            
                         autosize=True,
                         margin=dict(l=0,r=0,t=25,b=20)
                         )
    time.sleep(1)
    return (dcc.Graph(figure = fig))

       
 #AutoFiltering callbacks
        

#callback for date filtering
@app.callback(
        Output('Dropdown_2','options'),
        [Input('Dropdown_1','value')
         ]
    ) 
 
 
def update_date(month):
    day_dict = [day for day in range(1,32)]
    option = []
    if month:
        option = [{'label':m,'value':m} for m in day_dict]
    return option
    
    
    
#callback for country filtering    
@app.callback(
        Output('Dropdown_4','options'),
        [Input('Dropdown_3','value')
         ]
    )     

def update_country(region):
    
    option = []
    
    if region is None:
        raise PreventUpdate
        
    else:
        
        for r in region:
            
            if r in country_dict.keys():
                
                option.extend(country_dict[r])
                
    return [{'label':o , 'value':o} for o in option]
    
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['region_txt']==region] ['country_txt'].unique().tolist()] 


#callback for state filtering    
@app.callback(
        Output('Dropdown_5','options'),
        [Input('Dropdown_4','value')
         ]
    )     

def update_state(country):
    
    option = []
    
    if country is None:
        
        raise PreventUpdate
        
    else:
        
        for c in country:
            
            if c in state_dict.keys():
                
                option.extend(state_dict[c])
                
    return [{'label':o , 'value':o} for o in option]
        
        
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['country_txt']==country] ['provstate'].unique().tolist()] 

    
#callback for city filtering
@app.callback(
        Output('Dropdown_6','options'),
        [Input('Dropdown_5','value')
         ]
    )     

def update_city(state):
    
    option = []
    
    if state is None:
        
        raise PreventUpdate
            
    else:
        
        for s in state:
            
            if s in city_dict.keys():
                
                option.extend(city_dict[s])
                
    return [{'label':o , 'value':o}     for o in option]
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['provstate']==state] ['city'].unique().tolist()] 

    

#For India Map
#callback for map 
@app.callback(
        dash.dependencies.Output('loading_2', 'children'),
        
        [dash.dependencies.Input('Dropdown_a', 'value'),
         dash.dependencies.Input('Dropdown_b', 'value'),
         dash.dependencies.Input('Dropdown_c', 'value'),
         dash.dependencies.Input('Dropdown_d', 'value'),
         dash.dependencies.Input('Dropdown_e', 'value'),
         dash.dependencies.Input('Dropdown_f', 'value'),
         dash.dependencies.Input('Dropdown_g', 'value'),         
         dash.dependencies.Input('year_slider1','value')
         ]
    )
    

def update_ui1(dd1,dd2,dd3,dd4,dd5,dd6,dd7,slider):
    #best practices to print datatype and values of paramters passed
    print('\nDatatype of dd1:',type(dd1))
    print('Value of dd1:',str(dd1))
    
    print('\nDatatype of dd2:',type(dd2))
    print('Value of dd2:',str(dd2))
    
    print('\nDatatype of dd3:',type(dd3))
    print('Value of dd3:',str(dd3))
    
    print('\nDatatype of dd4:',type(dd4))
    print('Value of dd4:',str(dd4))
    
    print('\nDatatype of dd5:',type(dd5))
    print('Value of dd5:',str(dd5))
    
    print('\nDatatype of dd6:',type(dd6))
    print('Value of dd6:',str(dd6))
    
    print('\nDatatype of dd7:',type(dd7))
    print('Value of dd7:',str(dd7))
       
    print('\nDatatype of slider:',type(slider))
    print('Value of slider:',str(slider))
    
    
    #year_filter
    year_range = range (slider[0],slider[1]+1)
   
    new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

    new_df = df[df['iyear'].isin(year_range)]
    
    
    
    #blank figure
    fig = go.Figure()
    
    
    #month and day filter
    if  dd1 == [] or dd1 is None :
        
        pass
        
    
    else:
        
            if dd2 == [] or dd2 is None :
           
                new_df = new_df[new_df['imonth'].isin(dd1)]
                
            else:
                
                new_df = new_df[(new_df['imonth'].isin(dd1)) & 
                             (new_df['iday'].isin(dd2))
                             ]
    
        
    #region, country, state and city filter
    if dd3 == [] or dd3 is None:
        
        pass
    
    else:
        
        if dd4 == [] or dd4 is None:
            
            new_df = new_df[new_df['region_txt'].isin(dd3)]
            
        else:
            
            if dd5 == [] or dd5 is None:
                
                new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                (new_df['country_txt'].isin(dd4))
                                ]
            
            else:
                
                if dd6 == [] or dd6 is None:
            
                    new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                    (new_df['country_txt'].isin(dd4)) &
                                    (new_df['provstate'].isin(dd5))
                                    ]
            
                else:
                   
                    new_df = new_df[(new_df['region_txt'].isin(dd3)) & 
                                    (new_df['country_txt'].isin(dd4)) &
                                    (new_df['provstate'].isin(dd5)) &
                                    (new_df['city'].isin(dd6))
                                    ]
            
            
    #attack type filter
    if dd7 == [] or dd7 is None:
        
        pass
    
    else:
        
        new_df = new_df[new_df['attacktype1_txt'].isin(dd7)]
        
         
    #creating map   
    fig = px.scatter_mapbox(new_df,
                              lat='latitude',
                              lon='longitude',
                              hover_data=['iyear','region_txt','country_txt','provstate','city','nkill'],
                              color='attacktype1_txt',
                              labels=attack_dict,
                              height=800,
                              zoom=1
                              )
    
    fig.update_layout(mapbox_style='carto-darkmatter', 
                         legend=dict(orientation ='h',
                                    x=0,
                                    y=0,
                                    
                                    title_font_family="Times New Roman",
                                    font=dict(
                                        family="Courier",
                                        size=13.55,
                                        color="White"
                                    ),
                                    bgcolor="black",
                                    bordercolor="White",
                                    borderwidth=1
                                    ),                           
                         autosize=True,
                         margin=dict(l=0,r=0,t=25,b=20)
                         )
    time.sleep(1)
    return (dcc.Graph(figure = fig))


@app.callback(
        Output('Dropdown_b','options'),
        [Input('Dropdown_a','value')
         ]
    ) 
 
 
def update_date1(month):
    day_dict = [day for day in range(1,32)]
    option = []
    if month:
        option = [{'label':m,'value':m} for m in day_dict]
    return option
    
    
    
#callback for country filtering    
@app.callback(
        Output('Dropdown_d','options'),
        [Input('Dropdown_c','value')
         ]
    )     

def update_country1(region):
    
    option = []
    
    if region is None:
        raise PreventUpdate
        
    else:
        
        for r in region:
            
            if r in country_dict.keys():
                
                option.extend(country_dict[r])
                
    return [{'label':o , 'value':o} for o in option]
    
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['region_txt']==region] ['country_txt'].unique().tolist()] 


#callback for state filtering    
@app.callback(
        Output('Dropdown_e','options'),
        [Input('Dropdown_d','value')
         ]
    )     

def update_state1(country):
    
    option = []
    
    if country is None:
        
        raise PreventUpdate
        
    else:
        
        for c in country:
            
            if c in state_dict.keys():
                
                option.extend(state_dict[c])
                
    return [{'label':o , 'value':o} for o in option]
        
        
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['country_txt']==country] ['provstate'].unique().tolist()] 

    
#callback for city filtering
@app.callback(
        Output('Dropdown_f','options'),
        [Input('Dropdown_e','value')
         ]
    )     

def update_city1(state):
    
    option = []
    
    if state is None:
        
        raise PreventUpdate
            
    else:
        
        for s in state:
            
            if s in city_dict.keys():
                
                option.extend(city_dict[s])
                
    return [{'label':o , 'value':o}     for o in option]
    
    #return [ {'label':str(i),'value':str(i)}   for i in df[df['provstate']==state] ['city'].unique().tolist()] 




#callback for World Chart
@app.callback( Output('wc', 'children'),
              [Input('Dropdown_wc','value'),
               Input('search','value'),
               Input('year_slider1c','value')
               ]
              )

def update_chart(wc,search,sl1c):
    
    print('\n\nDatatype of World Chart value: ',type(wc))
    print('\nValue of World Chart: ',str(wc))
    print('\nValue of World slider: ',str(sl1c))
    print('\n\n')
    
    chartFigure = go.Figure()
    
    year_range1 = range(sl1c[0],sl1c[1]+1)
    
    df_wc = df[df['iyear'].isin(year_range1)]
    
    

    if wc is not None:
        
        if search is not None:
            
            df_wc = df_wc.groupby('iyear')[wc].value_counts().reset_index(name='Count')
            df_wc = df_wc[df_wc[wc].str.contains(search , case = False)]
            
        else:
            
            df_wc = df_wc.groupby('iyear')[wc].value_counts().reset_index(name='Count')
            
    else:
            
        raise PreventUpdate
            
        
             
    chartFigure = px.area(df_wc , x = 'iyear' , y = 'Count', color = wc , template="plotly_dark",
            color_discrete_sequence= px.colors.sequential.Plasma_r)
    
    fig = chartFigure
    time.sleep(1)
    return dcc.Graph(figure = fig)





#callback for India Chart
@app.callback( Output('ic', 'children'),
              [Input('Dropdown_ic','value'),
               Input('search_1','value'),
               Input('year_slider2c','value')
               ]
              )

def update_chart_1(ic,search,sl2c):
    
    print('\n\nDatatype of Indian Chart value: ',type(ic))
    print('\nValue of Indian Chart value: ',str(ic))
    print('\nValue of Indian slider: ',str(sl2c))
    print('\n\n')
    
    chartFigure = go.Figure()
    
    
    dfi = df.loc[(df['region_txt']=='South Asia') & (df['country_txt']=='India')  ]     #filtering Indian values
    
    year_range2 = range(sl2c[0] , sl2c[1]+1)

    df_ic = dfi[dfi['iyear'].isin(year_range2)]
    

    if ic is not None:
        
        if search is not None:
            
            df_ic = df_ic.groupby('iyear')[ic].value_counts().reset_index(name='Count')
            df_ic = df_ic[df_ic[ic].str.contains(search , case = False)]
            
        else:
            
            df_ic = df_ic.groupby('iyear')[ic].value_counts().reset_index(name='Count')
            
    else:
            
        raise PreventUpdate
            
    
            
    chartFigure = px.area(df_ic , x = 'iyear' , y = 'Count', color = ic , template="plotly_dark",
            color_discrete_sequence= px.colors.sequential.Plasma_r)
    
    fig = chartFigure
    time.sleep(1)
    return dcc.Graph(figure = fig)




#main function
def main():
    
    print('\n\n\tWelcome, the project starts in 3,2,1....\n')
    
    load_data()
    
    open_browser()
    
    global app
    app.layout=ui()
    app.title='Terrorism Analysis'
    
    
    #no code beyond this line
    app.run_server()
    print('\n\n\t***End of code***\n')
    
    global df
    print(df.columns)
    df=None
    app=None
   
    
    
    
    
    
if __name__ == '__main__':
    main()    
    