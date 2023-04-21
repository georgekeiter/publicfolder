# this code tests the concept that NHL Players tend to be born earlier in the year
# due to junior hockey rules which separate age groups by year.
# So players born in January have the advantage of being 11 months
# older than those born at the end of the year

import pandas as pd
import numpy as np
import scipy as sc

file = r'/Users/georgekeiter/Desktop/python/nhl_birth_month.csv'

df = pd.read_csv(file)
players_by_month = pd.DataFrame({'Month': df['Month'], 'Count of Players': df['Players']})


# In this function, input which month you want to test, and it will output a p-value
# that the month is different from the entire population. The for loop below
# performs the test for all 12 months. The results show, as expected, that January
# and December have the lowest p-values, while June/July are close to 1 (smallest possible)

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


# Below function allows you to directly compare 2 months.


def two_month_z_test(month1, month2):
    x1 = df.loc[df['Month'] == month1, 'Players'].sum()
    x2 = df.loc[df['Month'] == month2, 'Players'].sum()
    n1 = df['Players'].sum()
    n2 = n1
    p1 = x1 / n1
    p2 = x2 / n2
    p_diff = p1 - p2
    p_pool = (x1 + x2) / (n1 + n2)
    std_error = np.sqrt(p_pool * (1 - p_pool) * ((1 / n1) + (1 / n2)))
    z = p_diff / std_error
    p_value = 1 - sc.stats.norm.cdf(z)
    return p_value


# The below line tests whether January having more players than April
# in the NHL is statistically significant (to 6 decimal places).
# Please note that this is a one-sided test as opposed to the first function,
# so if you flipped Jan and April the p-value would be close to 1,
# meaning that there is almost no chance that people born in April
# are more likely to be in the NHL than those born in January.

print("{:.6f}".format(two_month_z_test('January', 'April')))
