import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data_unconverted.csv")
df = df.rename({"Unnamed: 0": "Keywords"}, axis="columns")
df = df.set_index("Keywords")

for index, col in df.items():
    if index == "Unnamed: 0":
        continue
    print(col.sum())
    col = col[col > 0]
    col = col.nlargest(30)

    ax = col.plot.bar(title=index)
    plt.show()
