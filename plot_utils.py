import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_skeletal_grain(fig,df,yaxis_title,row,col,showlegend=False,legendgroup=None):
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['min'],showlegend = False,
                                 fill=None,mode='lines',line_color='white',legendgroup=legendgroup
                            ),row=row,col=col)
    
    fig.add_trace(go.Scatter(x=df['time'],y=df['max'],showlegend = False,
                             fill='tonexty', # fill area between trace0 and trace1
                             mode='lines', fillcolor='rgba(174, 215, 234,0.5)',
                             line_color = 'white'),row=row,col=col)


    fig.add_trace(go.Scatter(x = df['time'],y = df['mean'],mode = 'lines+markers',
                             name = 'Mean', line = dict(color = 'black'),showlegend = showlegend,legendgroup=legendgroup,
                             marker = dict(color = 'black',size = 8),
                             #error_y=dict(type='data', array=data_skeletal['std'])
                             ),row=row,col=col)
    fig.add_trace(go.Scatter(x = df['time'],y = df['median'],mode = 'lines+markers',
                             name = 'Median', line = dict(color = 'black',dash = 'dot'),
                             showlegend = showlegend,legendgroup=legendgroup,
                             marker = dict(color = 'black',size = 8,symbol = 'diamond')
                             ),row=row,col=col)

    if col == 1:
        fig.update_yaxes(title = f'{yaxis_title} %',ticks = 'outside',showline = True, 
                         mirror = True,linecolor = 'black',row=row,col=col)
    else:
        fig.update_yaxes(ticks = 'outside',showline = True, 
                         mirror = True,linecolor = 'black',row=row,col=col)
    

    
def plot_time(fig,df,width,row,col):
    fig.add_trace(go.Bar(x = df['min_ma'], y = df['scale_no']*0.2,showlegend = False,
                    offset=0,width = width,marker_color = df['color'],
                    text = df.interval_name,textposition = 'inside',
                     x0 = 0,dx = 100,
                    textfont = dict(size = 12,color = 'black', family='Arial black')),
                  row=row,col=col)
    
    fig.update_yaxes(showticklabels = False,row=row,col=col)
    
def plot_skeletal_grain_nobounds(fig,df,yaxis_title,color,name,row,col,showlegend=False,size=8,mode='lines+markers',legendgroup=None):
    
    fig.add_trace(go.Scatter(x = df['time'],y = df['mean'],mode = mode,
                             name = name, line = dict(color = color),showlegend = showlegend,legendgroup=legendgroup,
                             marker = dict(color = color,size = size),
                             #error_y=dict(type='data', array=data_skeletal['std'])
                             ),row=row,col=col)
    #fig.add_trace(go.Scatter(x = df['time'],y = df['median'],mode = 'lines+markers',
    #                         name = 'Median', line = dict(color = color,dash = 'dash'),
    #                         showlegend = showlegend,
    #                         marker = dict(color = 'black',size = 8,symbol = 'diamond')
    #                         ),row=row,col=col)

    if col == 1:
        fig.update_yaxes(title = f'{yaxis_title} %',ticks = 'outside',showline = True, 
                         mirror = True,linecolor = 'black',row=row,col=col)
    else:
        fig.update_yaxes(ticks = 'outside',showline = True, 
                         mirror = True,linecolor = 'black',row=row,col=col)
    