import pandas as pd
import pyspark
from pyspark.sql import SparkSession
#print(pd.read_csv("users.csv"))
pd.read_csv("users.csv")
from pyspark.sql import SparkSession
spark=SparkSession.builder.appName("XP").getOrCreate()
spark
df_pyspark=spark.read.csv('users.csv')
df_pyspark