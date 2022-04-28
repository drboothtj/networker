import plotly.graph_objects as go

def plot_histogram(values, filename):
    figure = go.Figure(data=[go.Histogram(x=values, cumulative_enabled=True)])
    figure.write_html(filename)
