import pandas as pd

first_names = ['John', 'Tom', 'Fred', 'Michael', 'Andrew']

last_names = ['Turner', 'Harden', 'Bryant', 'Davis', 'Turner']

df = pd.DataFrame(list(zip(first_names, last_names)), columns=['First Name', 'Last Name'])

df2 = df[(df["First Name"].isin(["John"])) & (df["Last Name"].isin(["Turner"]))]

print(df2.loc[0, "First Name"])