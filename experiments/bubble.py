import plotly.express as px
import pandas as pd

df = pd.read_csv("../collect_data/final/Org_cats.csv")
print(df)
fig = px.scatter(df, x="category", y="Victim Count (Million)", color="category",
                 size="Victim Count (Million)", text="Number of Breaches")
fig.show()