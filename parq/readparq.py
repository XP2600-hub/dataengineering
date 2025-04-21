import pandas as pd
data = pd.read_parquet('users.parquet', engine='pyarrow')
pd.set_option('display.max_rows', None)
print(data)


