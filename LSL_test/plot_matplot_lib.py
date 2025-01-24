from matplotlib import pyplot as plt
import pandas as pd
import mne

df = pd.read_csv("EEGdata.csv")

cols = [1,2,3,4,5,6,7,8]

df = df[df.columns[cols]]

for label, column in df.items():
    items = column.to_numpy()
    data = mne.filter.filter_data(items, 250, 2, 40)

    print(label)
    plt.plot(data)
    plt.show()
