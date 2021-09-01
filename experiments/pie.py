import plotly.express as px
import pandas as pd

df = pd.read_csv("../collect_data/final/Org_cats.csv")

fig = px.pie(df, values='Victim Count (Million)', names='category')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
fig.show()