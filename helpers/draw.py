#    Copyright 2019 D-Wave Systems Inc.

# Imports both in modules and JN for users skipping sections
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import sys
from bokeh.io import show, output_notebook
from bokeh.models import Plot, Range1d, MultiLine, Circle, Label, LabelSet, ColumnDataSource
from bokeh.models import WheelZoomTool, ZoomInTool, ZoomOutTool, ResetTool, PanTool
from bokeh.models.graphs import from_networkx

me = sys.modules[__name__]
if not hasattr(me, 'bokeh_loaded'):
    output_notebook()
    bokeh_loaded = True

pos = {}	
def bqm_layout(G):
    """Little hack for compliancy with Bokeh version 0.12.15"""
    pos.update(nx.random_layout(G))
    return pos

def plot_bqm(bqm):
    """Plot binary quadratic model as a labeled graph."""
    g = nx.Graph()
    g.add_nodes_from(bqm.variables)
    g.add_edges_from([(edge[0], edge[1], {'edge_color': 'blue' if value == 1 else 'red'}) for edge, value in bqm.quadratic.items()])

    if len(bqm) < 25:
        plot_size = 300
        text_size = '16pt'
    else:
        plot_size = 700
        text_size = '12pt'
  
    pos.clear()
    graph = from_networkx(g, bqm_layout)
    graph.node_renderer.glyph = Circle(size=35, fill_color='yellow', fill_alpha=0.25)
    graph.edge_renderer.glyph = MultiLine(line_color='color', line_alpha=0.8, line_width=2)
    graph.edge_renderer.data_source.add([edge[2]['edge_color'] for edge in  g.edges.data()], 'color')
 
    data = {'xpos': [], 'ypos': [], 'label': []}
    for label, loc in pos.items():
        data['label'].append(label)
        data['xpos'].append(loc[0])
        data['ypos'].append(loc[1])
    labels = LabelSet(x='xpos', y='ypos', text='label', level='glyph', 
                      source=ColumnDataSource(data), x_offset=-8, y_offset=-8, 
                      text_color="black", text_font_size='16pt', text_font_style='bold')    
    
    plot = Plot(plot_width=plot_size, plot_height=plot_size, x_range=Range1d(-0.1, 1.1), y_range=Range1d(-0.2, 1.1))
    plot.title.text = "BQM with {} nodes and {} edges".format(len(bqm), len(bqm.quadratic))
    
    tools = [WheelZoomTool(), ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    plot.add_tools(*tools)
    plot.toolbar.active_scroll = tools[0]
    
    plot.renderers.append(graph)
    plot.add_layout(labels)
    plot.background_fill_color = "darkgrey"
    
    for lt1, lt2, lt3 in [[-0.125, "Blue edges have value 1", "blue"], [-0.195, "Red edges have value -1", "red"]]:
        legendtext = Label(x=-0.05, y=lt1, text=lt2,
                       text_color=lt3, text_font_size='12pt', text_font='Times')
        plot.add_layout(legendtext)
    
    show(plot)

def plot_hamming(hd):
    """Plot Hamming distances."""
    plt.figure(figsize=(6, 3*len(hd)))
    axis = 1
    for sampler, distance in hd.items():
        ax = "ax"+str(axis)
        ax = plt.subplot(len(hd), 1, axis)
        ax.set_title("Sampler: " + sampler)
        ax.set_xlabel("Sample")
        ax.set_ylabel("Normalized Hamming Distance")
        ax.plot(range(len(distance[0])), 100*distance[0], 'b', lw=.4)
        ax.plot([0, len(distance[0])], [100*distance[1], 100*distance[1]], 'black')  
        ax.yaxis.set_major_formatter(PercentFormatter())
        ax.set_ylim(0, 100)        
        axis += 1
    plt.tight_layout()

def plot_sig_ac(signals, corrs):
    """Plot pairs of signals and their autocorrelations."""  
    plt.figure(figsize=(10, 3*len(signals)))
    axis = 1
    for title, signal in signals.items():
        ax = "ax"+str(axis)
        ax = plt.subplot(len(signals), 2, axis)
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitude")        
        ax.plot(range(len(signal)), signal, 'g.')
        ax.plot([0, len(signal)], [np.mean(signal), np.mean(signal)], 'black')  
        axis += 1
        ax = "ax"+str(axis)
        ax = plt.subplot(len(signals), 2, axis)
        ax.set_title("Autocorrelated: " + title)
        ax.set_xlabel("Sample")
        ax.set_ylabel("Autocorrelation")         
        ax.plot(range(len(corrs.loc[corrs['Signal'] == title].ac.iat[0])), corrs.loc[corrs['Signal'] == title].ac.iat[0], 'b.') 
        ax.plot([0, len(corrs.loc[corrs['Signal'] == title].ac.iat[0])], [np.sqrt(np.mean(corrs.loc[corrs['Signal'] == title].ac.iat[0]**2)), np.sqrt(np.mean(corrs.loc[corrs['Signal'] == title].ac.iat[0]**2))], 'black')        
        axis += 1
    plt.tight_layout()

def plot_ac1(ac, x):
    plt.figure(figsize=(5, 3*len(ac)))
    axis = 0
    ax = [0 for i in range(len(ac))]
    y = [[0, 0] for i in range(len(ac))]
    for system, corr in ac.items():
        ax[axis] = plt.subplot(len(ac), 1, axis + 1)
        ax[axis].set_title("Sampler:" + system)
        ax[axis].set_xlabel(x)
        ax[axis].set_ylabel("Autocorrelation")
        ax[axis].plot(range(len(ac[system])), corr.ac1, 'b-o')        
        ax[axis].plot([0, len(ac[system])], [corr.ac1.mean(axis='index'), corr.ac1.mean(axis='index')], 'black')  
        y[axis] = ax[axis].get_ylim()
        axis += 1
    for axis in range(len(ac)):
        ax[axis].set_ylim(0.95*min([bottom[0] for bottom in y]), 1.05*max([top[1] for top in y])) 
    plt.tight_layout()


def plot_ac_lag(ac, lag=25):
    plt.figure(figsize=(5, 5))
    for system, corr in ac.items():
        mid = np.shape(ac[system]['ac'][0])[0]//2
        ac_lag = ac[system]['ac'][0][mid:mid+lag]
        ac1_lag = [ac[system]['ac1'][0]]
        for tile in range(1, len(ac[system])):
            ac_lag = np.vstack((ac_lag, ac[system]['ac'][tile][mid:mid+lag]))
            ac1_lag.append(ac[system]['ac1'][tile])
        ac_lag_avg = np.mean(ac_lag, axis=0)
        ac1_lag_avg = np.mean(ac1_lag)
        plt.errorbar(range(1, lag+1), ac_lag_avg, yerr=np.std(ac_lag, axis=0), label=system, marker='o')
        plt.plot(1, ac1_lag_avg, 'ro', markersize=10)
        plt.text(1+0.5, ac1_lag_avg, "ac1", fontsize=12)        
    plt.legend()
    plt.title("Autocorrelation on All Solution Tiles by Lag")
    plt.xlabel("Lag")
    plt.ylabel("Average Autocorrelation")


