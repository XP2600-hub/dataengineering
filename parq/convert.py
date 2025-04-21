import pandas as pd
df = pd.read_csv('users.csv')
df.to_parquet('users.parquet')