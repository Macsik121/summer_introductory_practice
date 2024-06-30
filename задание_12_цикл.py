import pandas as pd

# читаем файл с исходными данными
df = pd.read_csv(
  './17-18.csv',
  usecols=['Команда_1', 'Команда_2', 'счёт'],
)

clubs_lst = [
  'Спартак', 'ЦСКА', 'Зенит', 'ФК Краснодар', 'Ахмат', 'ФК Ростов', 'ФК Уфа', 'Локомотив', 'Рубин', 'Амкар', 'Урал', 'Анжи',
  'Арсенал', 'Динамо', 'ФК Тосно', 'СКА-Хабаровск',
]
cmn_df_cols = ['И', 'В', 'Н', 'П', 'ЗАБ', 'ПРОП', 'О']
home_df_cols = ['В_Д', 'Н_Д', 'П_Д', 'ЗАБ_Д', 'ПРОП_Д']
guest_df_cols = ['В_Г', 'Н_Г', 'П_Г', 'ЗАБ_Г', 'ПРОП_Г']
# формируем изначальный DataFrame, к которому будем прибавлять результаты каждой из встреч

# DataFrame с общими показателями команды
cmn_df = pd.DataFrame(
  [[0] * 7],
  columns=cmn_df_cols,
  index=clubs_lst,
  dtype='int32'
)

# DataFrame домашних игр
home_df = pd.DataFrame(
  [[0] * 5],
  columns=home_df_cols,
  index=clubs_lst,
  dtype='int32',
)

# DataFrame гостевых игр
guest_df = pd.DataFrame(
  [[0] * 5],
  columns=guest_df_cols,
  index=clubs_lst,
  dtype='int32',
)

def create_df_t1(score_dict):
  t1_cmn_df = pd.DataFrame(
    [[
      1,
      # подсчёт общего кол-ва
      # побед
      1 if score_dict['голы_к1'] > score_dict['голы_к2'] else
      0,
      # ничей
      1 if score_dict['голы_к1'] == score_dict['голы_к2'] else
      0,
      # поражение
      1 if score_dict['голы_к1'] < score_dict['голы_к2'] else
      0,
      # забитых мячей
      score_dict['голы_к1'],
      # пропущенных
      score_dict['голы_к2'],
      # подсчёт очков
      (3 if score_dict['голы_к1'] > score_dict['голы_к2'] else
      1 if score_dict['голы_к1'] == score_dict['голы_к2'] else
      0),
    ]],
    columns=cmn_df_cols,
    dtype='int32'
  )
  t1_home_df = pd.DataFrame([[
    1 if score_dict['голы_к1'] > score_dict['голы_к2'] else
    0,
    1 if score_dict['голы_к1'] == score_dict['голы_к2'] else
    0,
    1 if score_dict['голы_к1'] < score_dict['голы_к2'] else
    0,
    score_dict['голы_к1'],
    score_dict['голы_к2'],
  ]], columns=home_df_cols, dtype='int32')
  
  return [t1_cmn_df, t1_home_df]

def create_df_t2(score_dict):
  t2_cmn_df = pd.DataFrame(
    [[
      1,
      # подсчёт общего кол-ва
      # побед
      1 if score_dict['голы_к2'] > score_dict['голы_к1'] else
      0,
      # ничей
      1 if score_dict['голы_к2'] == score_dict['голы_к1'] else
      0,
      # поражение
      1 if score_dict['голы_к2'] < score_dict['голы_к1'] else
      0,
      # забитых мячей
      score_dict['голы_к2'],
      # пропущенных
      score_dict['голы_к1'],
      # подсчёт очков
      (3 if score_dict['голы_к2'] > score_dict['голы_к1'] else
      1 if score_dict['голы_к2'] == score_dict['голы_к1'] else
      0),
    ]],
    columns=cmn_df_cols,
    dtype='int32'
  )
  t2_guest_df = pd.DataFrame([[
    1 if score_dict['голы_к2'] > score_dict['голы_к1'] else
    0,
    1 if score_dict['голы_к2'] == score_dict['голы_к1'] else
    0,
    1 if score_dict['голы_к2'] < score_dict['голы_к1'] else
    0,
    score_dict['голы_к2'],
    score_dict['голы_к1'],
  ]], columns=guest_df_cols, dtype='int32')
  
  return [t2_cmn_df, t2_guest_df]

# начинаем пробегаться по исходному файлу с данными
for i in range(len(df)):
  # берём текущую строку
  row = df.iloc[i]
  # раскладываем счёт из данного в подготовленный к работе
  score = row.loc['счёт'].split('(')[0].split(':')
  score[1] = score[1][0] # иногда счёт гостевой команды попадается со "*"
  score_dict = {
    'голы_к1': int(score[0]),
    'голы_к2': int(score[1]),
  }
  # создаём DataFrame'ы, которые добавляют к финальном таблицм поочерёдно результаты данной встречи
  t1_df = create_df_t1(score_dict)
  t2_df = create_df_t2(score_dict)
  # само добавление
  # результат команды хозяев
  cmn_df.loc[row.loc['Команда_1']] += t1_df[0].iloc[0]
  home_df.loc[row.loc['Команда_1']] += t1_df[1].iloc[0]
  # результат команды гостей
  cmn_df.loc[row.loc['Команда_2']] += t2_df[0].iloc[0]
  guest_df.loc[row.loc['Команда_2']] += t2_df[1].iloc[0]

# соединям все три DataFrame'а в одну таблицу
final_df = pd.concat([cmn_df, home_df, guest_df], axis=1)

# меняем названия команд, потому что те, которые в .csv, не соответствуют таблице на сайте !
brand_new_club_titles = ['Спартак-Москва', 'ПФК ЦСКА', 'Зенит', 'Краснодар', 'Ахмат', 'Ростов', 'Уфа', 'Локомотив', 'Рубин', 'Амкар', 'Урал', 'Анжи', 'Арсенал', 'Динамо', 'Тосно', 'СКА-Хабаровск',]
final_df.insert(0, 'Команда', brand_new_club_titles)
final_df.index = list(range(1, 17))

# выводим финальную таблицу
print(final_df)
