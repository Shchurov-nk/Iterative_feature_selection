import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/raw/salts_water_basic_IR.csv", index_col=0)

one_line = df.head(1).T.reset_index()
one_line["index"] = one_line["index"].astype(float)

masks = pd.read_csv("data/masks/95_00_masks.csv", index_col=0)
mask = masks["Cu"]
masked = one_line[mask.values!=0]

fig = px.line(one_line, x="index", y=1)
fig.add_scatter(x=masked["index"], y=masked[1], mode='markers')
fig