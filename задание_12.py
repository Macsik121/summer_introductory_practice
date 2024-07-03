import psutil
import pandas as pd

# Читаем файл исходных данных
df = pd.read_csv('./' + '17-18'
                #  input('Введите сезон: ')
                    + '.csv')
print(df)
normal_club_titles = {
  'Спартак': 'Спартак-Москва',
  'Томь': 'Томь',
  'ФК Ростов': 'Ростов',
  'ЦСКА': 'ПФК ЦСКА',
  'Зенит': 'Зенит',
  'ФК Краснодар': 'Краснодар',
  'Ахмат': 'Ахмат',
  'ФК Ростов': 'Ростов',
  'ФК Уфа': 'Уфа',
  'Локомотив': 'Локомотив',
  'Рубин': 'Рубин',
  'Амкар': 'Амкар',
  'Урал': 'Урал',
  'Анжи': 'Анжи',
  'Арсенал': 'Арсенал',
  'Динамо': 'Динамо',
  'ФК Тосно': 'Тосно',
  'СКА-Хабаровск': 'СКА-Хабаровск',
  'Крылья Советов': 'Крылья Советов',
  'Терек': 'Терек',
  'Волга': 'Волга',
  'Кубань': 'Кубань',
  'ФК Оренбург': 'Оренбург',
  'Енисей': 'Енисей',
  '': '',
  '': '',
}

# Формируем DataFrame со счётом
score = df['счёт'].str.split('(', expand=True)
score = score[0].str.split(':', expand=True)

score[1] = score[1].str.replace('*', '')
score = score.astype(int)

# Переименовываем стобцы для удобства работы
score.columns = ['голы_к1', 'голы_к2']
df[['голы_к1', 'голы_к2']] = score[['голы_к1', 'голы_к2']]

# Исправляем недостатки файла с исходными данными(удаляем ненужные пробелы строк)
df['Команда_1'] = df['Команда_1'].str.strip()
df['Команда_2'] = df['Команда_2'].str.strip()

df['Команда_1'] = df['Команда_1'].apply(lambda x: normal_club_titles[x])
df['Команда_2'] = df['Команда_2'].apply(lambda x: normal_club_titles[x])

# Формируем столбцы, от которых будем отталкиваться в подсчётах
# Победы и пораржения команды 1
df['поб_к1'] = df['голы_к1'] > df['голы_к2']
df['пор_к1'] = df['голы_к1'] < df['голы_к2']

# Победы и поражения команды 2
df['поб_к2'] = df['голы_к2'] > df['голы_к1']
df['пор_к2'] = df['голы_к2'] < df['голы_к1']

# Ничьи
df['ничьи'] = df['голы_к1'] == df['голы_к2']

# ---------------- Всё готово, теперь подсчёт самих данных(без помощи циклов!) ---------------- #
# Динамически формирующаяся колонка с кол-вом игр
home_games_played = df[['Команда_1', 'голы_к1']].groupby('Команда_1').count()['голы_к1']
guest_games_played = df[['Команда_2', 'голы_к2']].groupby('Команда_2').count()['голы_к2']
games_played = home_games_played + guest_games_played
# print(games_played)

# Голы команд, всего голов
home_goals = df[['Команда_1', 'голы_к1']].groupby('Команда_1').sum()['голы_к1']
guest_goals = df[['Команда_2', 'голы_к2']].groupby('Команда_2').sum()['голы_к2']
goals_total = home_goals + guest_goals

# Пропущенные голы
home_missed_goals = df[['Команда_1', 'голы_к2']].groupby('Команда_1').sum()['голы_к2']
guest_missed_goals = df[['Команда_2', 'голы_к1']].groupby('Команда_2').sum()['голы_к1']
missed_goals_total = home_missed_goals + guest_missed_goals

# Победы
home_wins = df[['Команда_1', 'поб_к1']].groupby('Команда_1').sum()['поб_к1']
guest_wins = df[['Команда_2', 'поб_к2']].groupby('Команда_2').sum()['поб_к2']
total_wins = home_wins + guest_wins

# Поражения
home_defeats = df[['Команда_1', 'пор_к1']].groupby('Команда_1').sum()['пор_к1']
guest_defeats = df[['Команда_2', 'пор_к2']].groupby('Команда_2').sum()['пор_к2']
total_defeats = home_defeats + guest_defeats

# Ничьи
home_draws = df[['Команда_1', 'ничьи']].groupby('Команда_1').sum()['ничьи']
guest_draws = df[['Команда_2', 'ничьи']].groupby('Команда_2').sum()['ничьи']
total_draws = home_draws + guest_draws

# Очки
pts = total_wins * 3 + total_draws

# название колонок, помогающих сортировать таблицу при равном кол-ве очков команд
sort_helping_cols = {'lvl0': ['Разность з - п', 'Всего', 'В гостях'], 'lvl1': ['Разность з - п'] + ['З'] * 2}

# Формируем мультииндекс, чтобы добавить надписи "Всего", "Дома" и "В гостях", как на сайте
array = [[' '] + ['Всего'] * 6 + ['Дома'] * 4 + ['В гостях'] * 4 + sort_helping_cols['lvl0'],
          ['Команды', 'И', 'В', 'Н', 'П', 'З - П', 'О', 'В', 'Н', 'П', 'З - П', 'В', 'Н', 'П', 'З - П'] + sort_helping_cols['lvl1']
        ]
mi_array= pd.MultiIndex.from_arrays(array)

# Изначальные колонки с голами формируем в форму, предствленную на сайте
final_goals_total = goals_total.astype(str) + ' - ' + missed_goals_total.astype(str)
final_goals_home = home_goals.astype(str) + ' - ' + home_missed_goals.astype(str)
final_goals_guest = guest_goals.astype(str) + ' - ' + guest_missed_goals.astype(str)

# Формируем финальный DataFrame
final_df = pd.DataFrame({
  (' ', 'Команды'): pd.Series(pts.index).to_list(),
  ('Всего', 'И'): games_played,
  ('Всего', 'В'): total_wins,
  ('Всего', 'Н'): total_draws,
  ('Всего', 'П'): total_defeats,
  ('Всего', 'З - П'): final_goals_total,
  ('Всего', 'О'): pts,
  ('Дома', 'В'): home_wins,
  ('Дома', 'Н'): home_draws,
  ('Дома', 'П'): home_defeats,
  ('Дома', 'З - П'): final_goals_home,
  ('В гостях', 'В'): guest_wins,
  ('В гостях', 'Н'): guest_draws,
  ('В гостях', 'П'): guest_defeats,
  ('В гостях', 'З - П'): final_goals_guest,
  ('Разность з - п', 'Разность з - п'): goals_total - missed_goals_total,
  ('Всего', 'З'): goals_total,
  ('В гостях', 'З'): guest_goals,
}, columns=mi_array)

# Сортируем команды по очкам
sort_helping_cols_generated = [(sort_helping_cols['lvl0'][i], sort_helping_cols['lvl1'][i]) for i in range(len(sort_helping_cols['lvl0']))]
final_df.sort_values([('Всего', 'О'), ('Всего', 'В')] + sort_helping_cols_generated, inplace=True, ascending=False)

# удаляем вспомогательные для сортировки столбцы
final_df.drop(sort_helping_cols_generated, axis='columns', inplace=True)

# меняем индексы, имитируя номера мест команд
final_df.index = list(range(1, 16 + 1))

print(final_df)

print(psutil.Process().memory_info().rss)