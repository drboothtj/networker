'''
Plot graphs using plotly

Functions:
    plot_histogram(values, filename)
'''

import plotly.graph_objects as go

def plot_histogram(values, filename):
    '''Plots a histogram from a list of values and saves as an interactive .html file'''
    figure = go.Figure(data=[go.Histogram(x=values, cumulative_enabled=True)])
    figure.write_html(filename)
