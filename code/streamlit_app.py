import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/parsed/described.csv", index_col=0)
masks = pd.read_csv("data/masks/95_00_masks.csv", index_col=0)

def plot_masked_spectrum(df, masks):
    one_line = df.T.reset_index()
    one_line["index"] = one_line["index"].astype(float)

    mask = masks["Cu"]
    masked = one_line[mask.values!=0]

    line_plot = px.line(one_line, x="index", y=["min", "50%", "max"], color_discrete_sequence=["green", "blue", "orange"])
    scatter_plot = px.scatter(masked, x='index', y='50%', title='Scatter Plot', color_discrete_sequence=['red'], width=100)
    line_plot.add_trace(scatter_plot.data[0])
    return line_plot
line_plot = plot_masked_spectrum(df, masks)
line_plot

# TODO use fig = go.Figure() instead
# fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
#                          name=labels[i],
#                          line=dict(color=colors[i], width=line_size[i]),
#                          connectgaps=True,
#                          ))

def plot_corr_xx(corr_xx):
    corr_xx.columns = corr_xx.columns.astype(float)
    fig = px.imshow(
        corr_xx.iloc[0::5, 0::5], 
        color_continuous_scale='YlOrRd', 
        labels={'x': "Wavenumber, cm⁻¹"})
    fig.update_layout(
        xaxis={'side': 'top'}, 
        yaxis={'side': 'left'}
        )
    return fig

corr_xx = pd.read_csv("data/corr/XX_dist.csv", index_col=0)
corr_xx_plot = plot_corr_xx(corr_xx)
corr_xx_plot