import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./17-18.csv', usecols=['Дата', 'Команда_1', 'Команда_2', 'счёт'])

score = df['счёт'].str.split(':', expand=True)
del score[2]

score.iloc[:, 1] = score.iloc[:, 1].str.split('(', expand=True).iloc[:, 0]
score = score.apply(lambda x: x.apply(lambda y: int(y) if '*' not in y else int(y[0])))

score.columns = ['голы_к1', 'голы_к2']
df[['голы_к1', 'голы_к2']] = score[['голы_к1', 'голы_к2']]

print(df)
plt.plot([1, 2, 5, 9])
plt.show()
