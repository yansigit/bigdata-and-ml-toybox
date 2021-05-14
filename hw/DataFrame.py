import pandas as pd

df = pd.DataFrame(data = [[500,450,520,610],
                     [690, 700, 820, 900],
                     [1100, 1030, 1200, 1380],
                     [1500, 1650, 1700, 1850],
                     [1990, 2020, 2300, 2420],
                     [1020, 1600, 2200, 2550]], index = [a for a in range(2015, 2021)], columns= [a for a in range(1, 5)])

print(df)

df.to_csv('term1.csv')