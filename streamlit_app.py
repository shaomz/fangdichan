import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

hide_streamlit_style = """
<style>
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

@st.cache_data
def get_data():
    source = pd.read_csv('baoyouliang.csv')
    return source

stock_data = get_data()
st.dataframe(stock_data)
hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

lines = (
    alt.Chart(stock_data, theme='streamlit',title="一手房存量")
    .mark_line()
    .encode(
        x="date",
        y="first"
    )
)

points = lines.transform_filter(hover).mark_circle(size=65)

tooltips = (
    alt.Chart(stock_data)
    .mark_rule()
    .encode(
        x="yearmonthdate(date)",
        y="first",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("date", title="时间"),
            alt.Tooltip("first", title="一手房存量(套)"),
        ],
    )
    .add_selection(hover)
)

data_layer = lines + points + tooltips

# ANNOTATIONS = [
#     ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
#     ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
#     ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
#     ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
# ]
# annotations_df = pd.DataFrame(
#     ANNOTATIONS, columns=["date", "price", "marker", "description"]
# )
# annotations_df.date = pd.to_datetime(annotations_df.date)

# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=20, dx=-10, dy=0, align="left")
#     .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
# )

combined_chart = data_layer 
# + annotation_layer
st.altair_chart(combined_chart,theme='streamlit',use_container_width=True)
