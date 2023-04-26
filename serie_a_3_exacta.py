import pandas as pd
from sklearn.linear_model import LinearRegression

lr = LinearRegression()

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

file = r'/Users/georgekeiter/Desktop/python/seriea_2122.csv'
sfile = r'/Users/georgekeiter/Desktop/python/seriea_o25o35_sample.csv'

df = pd.read_csv(file)

goals = df['FTHG'] + df['FTAG']
o2_5 = goals > 2
u3_5 = goals < 4

df = pd.read_csv(file, usecols=['Avg>2.5'])
sdf = pd.read_csv(sfile)
sdf = sdf.drop('game', axis=1)

p_df = 1 / df
p_sdf = 1 / sdf

lr.fit(p_sdf[['Avg>2.5']], p_sdf['Avg<3.5'])

p_df['est<3.5'] = lr.intercept_ + (lr.coef_ * p_df['Avg>2.5'])

df['est<3.5'] = round(1 / p_df['est<3.5'], 2)


def calculate_stake_flat(odds):
    if odds >= 2:
        return 100
    else:
        return (1 / (odds - 1)) * 100


df['stake2_5'] = df['Avg>2.5'].apply(calculate_stake_flat)
df['stake3_5'] = df['est<3.5'].apply(calculate_stake_flat)
df['o2.5'] = o2_5
df['u3.5'] = u3_5

def outcome_flat(row):
    if row['o2.5'] and row['u3.5']:
        return row['stake2_5'] * (row['Avg>2.5'] - 1) + row['stake3_5'] * (row['est<3.5'] - 1)
    elif row['o2.5'] and not row['u3.5']:
        return row['stake2_5'] * (row['Avg>2.5'] - 1) - row['stake3_5']
    elif row['u3.5'] and not row['o2.5']:
        return row['stake3_5'] * (row['est<3.5'] - 1) - row['stake2_5']
    else:
        return -1 * (row['stake2_5'] + row['stake3_5'])


df['outcome_flat'] = round(df.apply(outcome_flat, axis=1), 2)

# delete torino fiorentina jan 9 2022 bad data
df = df.drop(203)

# using this method of staking to reach $100 profit,
# the outcome is a loss of $5,772.20 across $148,357.64 of risk,
# or a loss of 3.89%. Next I will attempt to calculate a more favorable and varied staking approach
