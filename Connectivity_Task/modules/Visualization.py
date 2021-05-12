import plotly.express as px


def plotly_line(df, x, y, color, title):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    return fig


def plotly_bar(df, x, y, color, title):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig.update_xaxes(type='category')
    return fig
