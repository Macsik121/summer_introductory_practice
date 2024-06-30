import pandas as pd
import numpy as np

dict_arr = {
  'age': [53, 26, 76, 43, 75],
  'name': ['Фам_1 Им_1 Отч_1', 'Фам_2 Им_2', 'Фам_3 Им_3', 'Фам_4 Им_4', 'Фам_5 Им_5',],
  'owns_car': [True, True, False, True, False],
}
df = pd.DataFrame(dict_arr)
def divide_name_col(series):
  user_names = series.str.split(' ').iloc[0]
  if len(user_names) == 2:
    user_names.append(np.nan)
  return user_names

names_series = df[['name']].apply(divide_name_col, axis=1, result_type='expand')
df[['Фамилия', 'Имя', 'Отчество']] = names_series
print(df)
# df['Фам', "Имя", "Отч"] = df['name'].str.split(' ')
