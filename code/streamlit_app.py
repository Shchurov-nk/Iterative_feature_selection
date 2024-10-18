import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/parsed/described.csv", index_col=0)

one_line = df.T.reset_index()
one_line["index"] = one_line["index"].astype(float)

masks = pd.read_csv("../data/masks/95_00_masks.csv", index_col=0)
mask = masks["Cu"]
masked = one_line[mask.values!=0]

line_plot = px.line(one_line, x="index", y=["min", "50%", "max"], color_discrete_sequence=["green", "blue", "orange"])
scatter_plot = px.scatter(masked, x='index', y='50%', title='Scatter Plot', color_discrete_sequence=['red'], width=100)
line_plot.add_trace(scatter_plot.data[0])
line_plot