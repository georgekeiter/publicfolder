import pandas as pd
import numpy as np
import scipy as sc

file = r'/Users/georgekeiter/Desktop/python/nhl_birth_month.csv'

df = pd.read_csv(file)
players_by_month = pd.DataFrame({'Month': df['Month'], 'Count of Players': df['Players']})


def z_test_month(month):
    p1 = df.loc[df['Month'] == month, 'Players'].sum() / df['Players'].sum()
    p = (1 / 12)

    x1 = df.loc[df['Month'] == month, 'Players'].sum()
    x2 = df['Players'].sum() - x1
    n = x1 + x2

    std_dev = np.std(df['Players'])

    z = (x1 - (n * p)) / std_dev

    p_val = round(2 * (1 - sc.stats.norm.cdf(abs(z))), 4)
    return p_val


months = df['Month']
for month in months:
    month_p_value = z_test_month(month)
    print(f"{month} two-tailed p-value = {month_p_value}")


"""print('January one-tailed p-value =', p_value, ': With a p-value just above 0.05, we cannot reject '
                                                   'the Ho that there is a statistically significant '
                                                   'amount of players born in January, or higher '
                                                   'chance that someone born in January compared '
                                                   'to any month will be in the NHL.')"""
