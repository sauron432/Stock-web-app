import plotly.graph_objects as go
import pandas as pd

def plotly_table(df, max_height=400):
    index_vals = [str(i)[:10] for i in df.index.tolist()]
    
    col_names = ["Date"] + df.columns.tolist()
    col_values = [index_vals] + [df[col].tolist() for col in df.columns]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=col_names,
                    fill_color="#2e2a1e",
                    font=dict(color="#f0c040", size=13),
                    align="left",
                    line_color="#2e2a1e",
                    height=36,
                ),
                cells=dict(
                    values=col_values,
                    fill_color=[["#1a1812", "#232018"] * len(df)],
                    font=dict(color="#f0c040", size=12),
                    align=["left"] + ["right"] * len(df.columns),
                    line_color=["#1a1812", "#232018"],
                    height=32,
                ),
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max_height,
    )

    return fig