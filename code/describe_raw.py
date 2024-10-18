import pandas as pd
import numpy as np
df = pd.read_csv("data/raw/salts_water_basic_IR.csv", index_col=0)
described_df = df.describe(percentiles=[0.05, 0.95])
described_df.drop(["mean", "std", "count"], inplace=True)
described_df.to_csv("data/parsed/described.csv")