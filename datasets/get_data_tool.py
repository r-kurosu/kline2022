import pandas as pd

for i in range(7, 12):
    df = pd.read_excel('BRA_6-11.xlsx', sheet_name=f"{i}dk")
    df.to_csv(f'BRA_{i}dk.csv', index=False)