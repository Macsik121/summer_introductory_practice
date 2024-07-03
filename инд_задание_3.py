import matplotlib.pyplot as plt
import pandas as pd

t_name = input('Введите название команды: ')
df = pd.read_csv('./' + input('Введите номер сезона в формате xx-xx: ') + '.csv',
                 usecols=['Дата', 'Команда_1', 'Команда_2', 'счёт'])

score = df['счёт'].str.split('(', expand=True)
score = score[0].str.split(':', expand=True)
score[1] = score[1].str.replace('*', '')
score = score.astype(int)

score.columns = ['голы_к1', 'голы_к2']
df[['голы_к1', 'голы_к2']] = score[['голы_к1', 'голы_к2']]

df['Команда_1'] = df['Команда_1'].str.strip()
df['Команда_2'] = df['Команда_2'].str.strip()

df['З - П разница к1'] = df['голы_к1'] - df['голы_к2']
df['З - П разница к2'] = df['голы_к2'] - df['голы_к1']

final_t_data1 = df[ df['Команда_1'] == t_name ][['Дата', 'Команда_1', 'З - П разница к1']]
final_t_data1.rename(columns={'Команда_1': 'КОМАНДА', 'З - П разница к1': 'З - П разница'}, inplace=True)
final_t_data2 = df[ df['Команда_2'] == t_name ][['Дата', 'Команда_2', 'З - П разница к2']]
final_t_data2.rename(columns={'Команда_2': 'КОМАНДА', 'З - П разница к2': 'З - П разница'}, inplace=True)
final_t_data = final_t_data1.merge(final_t_data2, how='outer')

final_t_data['Дата']=final_t_data['Дата'].astype('datetime64[ns]')
# final_t_data['Дата']=final_t_data['Дата'].astype(str)
final_t_data=final_t_data.sort_values(['Дата'])

print(final_t_data)
# fig, axes = plt.subplots(2, 2, figsize=(15, 8), dpi=200)
lbls = plt.plot(final_t_data['Дата'].to_list(), final_t_data['З - П разница'].to_list())
plt.title('Разница забитых и пропущенных голов команды ' + t_name + ' по датам')
plt.xticks(rotation=45)
plt.grid()
plt.show()
