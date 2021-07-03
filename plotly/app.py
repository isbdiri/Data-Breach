import plotly.express as px
import pandas as pd

group_by_year = pd.read_csv("../collect_data/final/year_bar_chart.csv")
scatter_data = pd.read_csv("../collect_data/final/scatter_data.csv")

fig = px.bar(group_by_year, x="year", y="Date")
fig.show()

fig = px.scatter(scatter_data, x="employee_count", y="exposure_index", color="category",
                 hover_data=['Org'])
fig.show()
