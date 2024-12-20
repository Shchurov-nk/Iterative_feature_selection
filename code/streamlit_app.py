import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/parsed/described.csv", index_col=0)
# masks = pd.read_csv("data/masks/masks.csv", index_col=0)
masks = pd.read_feather("data/masks/masks.feather")

element = st.selectbox(
    label="Select ion",
    options=masks["Element"].unique()
    )

Txx = st.slider(
    label="Redundancy: higher is more redundant features. Txx value", 
    min_value=0.90, 
    max_value=0.995, 
    value=0.95,
    step=0.005,
    format="%f"
    )
Txy = st.slider(
    label="Relevance: higher is more relevant features. Txy value", 
    min_value=0.0, 
    max_value=0.25, 
    value=0.0,
    step=0.05,
    format="%f"
    )

mask = masks.loc[(masks["Element"] == element) & (masks["T_xx"] == Txx) & (masks["T_xy"] == Txy)]
mask = mask.iloc[:, 4:].values[0]

def plot_masked_spectrum(df, mask):
    one_line = df.T.reset_index()
    one_line["index"] = one_line["index"].astype(float)
    x = one_line['index'].tolist()
    min = one_line['min'].tolist()
    per5 = one_line["5%"].tolist()
    mid = one_line['50%'].tolist()
    per95 = one_line["95%"].tolist()
    max = one_line['max'].tolist()

    masked = one_line[mask!=0]

    x_masked = masked["index"].tolist()
    mid_masked = masked["50%"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x + x[::-1],
            y=min + max[::-1],
            fill='toself',
            fillcolor='rgba(67,145,255,0.25)',
            line_color='rgba(67,145,255,0.3)',
            name='Min, Max'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x + x[::-1],
            y=per5 + per95[::-1],
            fill='toself',
            fillcolor='rgba(67,145,255,0.45)',
            line_color='rgba(67,145,255,0.45)',
            name='5%, 95% percentiles'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x + x[::-1],
            y=mid + mid[::-1],
            line_color='rgba(0,63,152,1)',
            name='Median'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_masked,
            y=mid_masked,
            mode='markers',
            marker_color='black',
            name='Selected channels'
        )
    )
    fig.update_layout(
        title="Infared spectrum, selected channels",
        xaxis_title="Wavenumber, cm⁻¹",
        yaxis_title="Absorption"
    )
    return fig

masked_spectrum = plot_masked_spectrum(df, mask)
st.plotly_chart(masked_spectrum, use_container_width=True)

# TODO: Нарисовать точку - выбранный сейчас порог

num_selected_df = masks[["Element", "T_xx", "T_xy", "Num_of_selected"]]
num_selected_df = num_selected_df[num_selected_df["Element"] == element].drop(columns="Element")

def plot_heatmap_num_of_selected(df):
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            x = df["T_xx"],
            y = df["T_xy"],
            z = df["Num_of_selected"]
            )
        )
    fig.update_layout(
        title="Infared spectrum, number of selected channels",
        xaxis_title="Txx value (Redundancy)",
        yaxis_title="Txy value (Relevance)"
    )
    return fig

heatmap_num_of_selected = plot_heatmap_num_of_selected(num_selected_df)
heatmap_num_of_selected



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
st.plotly_chart(corr_xx_plot, use_container_width=True)


