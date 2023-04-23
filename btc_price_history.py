import pandas as pd
import matplotlib as lib

path = r'/Users/georgekeiter/Desktop/python/btc_price_history.csv'
df = pd.read_csv(path)
df['Month'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.month
df['Day'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.day
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.date

mean1 = df['Open'].mean()
median1 = df['Open'].median()
std_dev1 = df['Open'].std()
var1 = std_dev1 ** 2
low1 = df['Open'].min()
high1 = df['Open'].max()

descr_stat = {'Average $': mean1, 'Median': median1, 'var': var1, 'std_dev': std_dev1}
descr_stat = pd.DataFrame.from_dict(descr_stat, orient='index', columns=['Value']).round(2)
descr_stat.index.name = 'STATS'
pd.options.display.float_format = '{:,.2f}'.format

print(descr_stat)

ms = df.groupby('Month').agg({'Open': ['count', 'min', 'max', 'mean', 'std']})
ms = ms.rename(columns={'count': 'n'})
print(ms)

max_date = df.loc[df['Open'].idxmax()]

print(max_date)

daily = df[['Date', 'Open']]
daily = daily.sort_values('Date', ascending=True)
daily.plot(kind='line', x='Date', y='Open')
lib.pyplot.xlabel('time')
lib.pyplot.ylabel('USD ($)')
lib.pyplot.title('btc price over time  mar 8 2019 to apr 18 2023')
lib.pyplot.show()
