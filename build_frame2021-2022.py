# %%
#%load_ext cudf.pandas

# %% [markdown]
# ### merge 2020 year frame
# 

# %%
import os
import pandas as pd

# %%
df1 = pd.read_excel('./data3/es/2020_new_base.xlsx')
df2 = pd.read_excel('./data3/es/2020_old_base.xlsx')

# %%
df1.columns==df2.columns


# %%
common_rows = pd.merge(df2, df1, how='inner')
common_rows

# %%
df3 = pd.concat([df1, df2],ignore_index=True)
df3

# %%
df3.to_excel('./data3/es/2020.xlsx', index=False)

# %% [markdown]
# ### read data

# %%
df2018 = pd.read_excel('./data3/es/2018.xlsx')
df2019 = pd.read_excel('./data3/es/2019.xlsx')
df2020 = pd.read_excel('./data3/es/2020.xlsx')
df2021 = pd.read_excel('./data3/es/2021.xlsx')

df2022_23 = pd.read_csv('./data3/predict/test_data.csv')

# %%
print(df2018.shape)
print(df2019.shape)
print(df2020.shape)
print(df2021.shape)
print(df2018.shape[0]+df2019.shape[0]+df2020.shape[0]+df2021.shape[0])

# %% [markdown]
# ### Data for training description
# Модель будет построена для предсказания значений в следующем году на основе полных данных за предыдущий год
# 
# Т.е:
# 
# Так как даные TR есть только начиная с 2018 года, решено отказаться от даных ранее 2018.
# Тренировочные датасеты строятся следующим образом:
# 
# 2018 -predict-> 2019
# 
# 2019 -predict-> 2020
# 
# 2020 -predict-> 2021

# %%
df2022_23_col = df2022_23.columns 

# %%
df2022_23  

# %%
df2018.columns

# %%
df2022_23.columns = ['code_discription', 'address_raw', 'data_short', 'cost']
df2022_23['test']=None

# %% [markdown]
# ### split test on 2022 and 2023

# %%
df2022_23['data_short'] = pd.to_datetime(df2022_23['data_short'], format='%m %Y')

# Сохраняем индекс для восстановления порядка строк
df2022_23['save_index']=df2022_23.index

# Разделяем DataFrame на два по годам
df_2022 = df2022_23[df2022_23['data_short'].dt.year == 2022].copy()
df_2023 = df2022_23[df2022_23['data_short'].dt.year == 2023].copy()



# Восстанавливаем исходный порядок строк
df_2022.sort_index(inplace=True)
df_2023.sort_index(inplace=True)

df_2022.to_excel('./data3/predict/2022.xlsx', index=False)
df_2023.to_excel('./data3/predict/2023.xlsx', index=False)


# %%
def check_same_values(col_name):
    print("check column: ", col_name)
    df2022_23_addr = df2022_23[col_name].unique()
    df2021_addr = df2021[col_name].unique()
    df2020_addr = df2020[col_name].unique()
    df2019_addr = df2019[col_name].unique()
    df2018_addr = df2018[col_name].unique()
    print("unique names:")
    print("2022_23: ",len(df2022_23_addr))    
    print("2021: ",len(df2021_addr))
    print("2020: ",len(df2020_addr))
    print("2019: ",len(df2019_addr))
    print("2018: ",len(df2018_addr))
    print("unique names cross")
    print("2018 vs 2019 ",len(list(set(df2018_addr) & set(df2019_addr))))
    print("2019 vs 2020 ",len(list(set(df2019_addr) & set(df2020_addr))))
    print("2020 vs 2021 ",len(list(set(df2020_addr) & set(df2021_addr))))
    print("2022-23 vs 2021 ",len(list(set(df2022_23_addr) & set(df2021_addr))))
    print("2022-23 vs 2020 ",len(list(set(df2022_23_addr) & set(df2020_addr))))
    print("2022-23 vs 2019 ",len(list(set(df2022_23_addr) & set(df2019_addr))))
    print("2022-23 vs 2018 ",len(list(set(df2022_23_addr) & set(df2018_addr))))


# %%
check_same_values('code_discription')

# %%
check_same_values('address_raw')

# %%
check_same_values('test')

# %%
df2022_23['code_discription'].unique()

# %%
all_es_types = {1:['Электроэнергия','Оплата потребления электроэнергии','Расходы по оплате потребления электроэнергии','Оплата за дизельное топливо','Оплата за электроэнергию по тарифам','Оплата за эектроэнергию по тарифам','Плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом'],
            2:['Отопление','Оплата всех видов отопления зданий и сооружений (кроме электро- и газового снабжения)','Расходы по оплате всех видов отопления зданий и сооружений (кроме электро- и газового снабжения)','Оплата за тепловую энергию по тарифам','Оплата за прочие виды топлиа (уголь, дрова и т.д.)'],
            3:['Водоснабжение','Оплата услуг водоснабжения, водоотведения','Расходы по оплате услуг водоснабжения, водоотведения','Оплата за водоотведение по тарифам','Оплата за горячее водоснабжение по тарифам','Оплата за холодное водоснабжение по тарифам', 'Оплата за холодное водоснабжение  по тарифам','Оплата за горячее  водоснабжение по тарифам','Оплата водоотведения по тарифам'],
            4:['Коммунальные услуги (расходы прошлых лет)','Коммунальные услуги (расходы прошлых лет)','Расходы на коммунальные услуги (расходы прошлых лет)','Другие расходы прошлых лет, выявленные в текущем году.','Другие расходы прошлых лет, выявленные в текущем году.'],
            5:['Газ','Оплата потребления газа','Расходы по оплате потребления газа','Оплата потребления газа по тарифам']}

def get_type_of_es(row):
    values_to_check = row[['code_discription', 'address_raw']]
    for key, values in all_es_types.items():
        if any(value.lower() in ' '.join(values_to_check.values).lower() for value in values):
            return key
    return None

#Usage: df['es_code_int'] = df.apply(get_type_of_es, axis=1)

# %%
df2022_23['es_code_int'] = df2022_23.apply(get_type_of_es, axis=1)

# %%
df2021['code_discription'].unique()


# %%
df2020['code_discription'].unique()

# %%
for i in df2018['address_raw']:
    if not ('Оплата за водоотведение по тарифам' in i or 'топливо ' in i or 'Оплата за горячее водоснабжение по тарифам' in i or 'Оплата за тепловую энергию по тарифам' in i or 'Оплата за холодное водоснабжение по тарифам'in i or 'Оплата за электроэнергию по тарифам'in i or 'Оплата за холодное водоснабжение  по тарифам' in i or 'Оплата за горячее  водоснабжение по тарифам' in i or 'Оплата за эектроэнергию по тарифам'in i
            or 'Оплата водоотведения по тарифам'in i or 'Другие расходы прошлых лет, выявленные в текущем году.' in i or 'Оплата потребления газа по тарифам'in i or 'Плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом' in i or 'Оплата за прочие виды топлиа (уголь, дрова и т.д.)' in i):
        print(i)

for i in df2019['address_raw']:
    if not ('Оплата за водоотведение по тарифам' in i or 'топливо ' in i or 'Оплата за горячее водоснабжение по тарифам' in i or 'Оплата за тепловую энергию по тарифам' in i or 'Оплата за холодное водоснабжение по тарифам'in i or 'Оплата за электроэнергию по тарифам'in i or 'Оплата за холодное водоснабжение  по тарифам' in i or 'Оплата за горячее  водоснабжение по тарифам' in i or 'Оплата за эектроэнергию по тарифам'in i
            or 'Оплата водоотведения по тарифам'in i or 'Другие расходы прошлых лет, выявленные в текущем году.' in i or 'Оплата потребления газа по тарифам'in i or 'Плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом' in i or 'Оплата за прочие виды топлиа (уголь, дрова и т.д.)' in i):
        print(i)
       

# %%
df2022_23.code_discription.unique()

# %%
check_same_values('address_raw')

# %%
check_same_values('es_code_int')

# %% [markdown]
# ### prep functions

# %%
#append clean addr
import re
def to_lower(listin):
    return [str(element).lower() for element in listin]

citys = pd.read_excel('./extra/np-dvfo.xlsx', header=None)[0].to_list()
streets = pd.read_excel('./extra/names-dvfo.xlsx', header=None)[0].to_list()
numbers = [str(i) for i in range(1, 1000)]
citys = to_lower(citys)
streets = to_lower(streets)
numbers = to_lower(numbers)

def clean_address(df, addr_col, new_addr_col):
    df[addr_col] = df[addr_col].str.lower()
    df[new_addr_col]=df[addr_col]
    df[new_addr_col] = df[new_addr_col].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))
    df[new_addr_col] = df[new_addr_col].apply(lambda x: ' '.join(word for word in x.split() if word in citys or word in streets or word in numbers))
    return df

# %%
#fuzzy compare address
from collections import Counter
from thefuzz import fuzz

def count_same_digits(array1, array2):
    if (len(array1)+len(array2))<2:
        return 0
    counter1 = Counter(array1)
    counter2 = Counter(array2)
    # Find the intersection considering duplicates
    common_elements = counter1 & counter2

    # Calculate the total count of common elements considering duplicates
    count_of_common_elements = sum(common_elements.values())
    #print(count_of_common_elements, len(array1), len(array2))
    
    return 2*count_of_common_elements/(len(array1)+len(array2))

def spec_match(str1, str2):
    digits_str1 = [int(d) for d in re.findall(r'\d+', str1)]
    digits_str2 = [int(d) for d in re.findall(r'\d+', str2)]
    dist = fuzz.WRatio(re.sub(r'\d', '', str1), re.sub(r'\d', '', str2))
    return dist*count_same_digits(digits_str1, digits_str2)/100.0

# %% [markdown]
# ### append data

# %%


# %%
df = df_2022[['code_discription', 'address_raw', 'data_short', 'cost']].copy()
df2 = df2021.copy()
df['address_raw'] = df['address_raw'].str.lower()
df2['address_raw'] = df2['address_raw'].str.lower()
set(df['address_raw'])&set(df2['address_raw'])

# %%
df

# %%
df2['data_short']=df2['data_short'].astype(str)
df2['data_short'] = pd.to_datetime(df2['data_short'], format='%m.%Y')
# Создаем столбец 'month'
df2['month'] = df2['data_short'].dt.month

# Создаем столбец 'year'
df2['year'] = df2['data_short'].dt.year
df2

# %%
df['es_code_int'] = df.apply(get_type_of_es, axis=1)

# %%
df = clean_address(df, 'address_raw', 'test')

# %%
df['data_short']=df['data_short'].astype(str)
df['data_short'] = pd.to_datetime(df['data_short'], format='%Y-%m-%d')
# Создаем столбец 'month'
df['month'] = df['data_short'].dt.month

# Создаем столбец 'year'
df['year'] = df['data_short'].dt.year
df

# %%
df['month']

# %%
len(set(df['address_raw'])&set(df2['address_raw']))

# %%
df['index_save'] = df.index

# %%
# Используем метод merge для объединения DataFrame на основе условия
df3 = df2[['address_raw', 'es_code_int','month','cost']].copy()
df3 = df3.groupby(['address_raw', 'es_code_int','month'], as_index=False)['cost'].mean()
merged_df = pd.merge(df, df3, on=['address_raw', 'es_code_int','month'], how='left', suffixes=('', '_prev_year'))

# В результате получаем новый DataFrame с добавленными данными
print(df.shape, df2.shape)
print(merged_df.columns, '\n',merged_df.shape)

# %%
nan_rows_merged_df = merged_df[merged_df['cost_prev_year'].isna()]
nan_rows_merged_df.shape

# %%
merged_df = merged_df.dropna(subset=['cost_prev_year'])
merged_df.shape

# %%
nan_rows_merged_df.drop(columns=['cost_prev_year'], inplace=True)
shift_value = 1
nan_rows_merged_df['month'] = (nan_rows_merged_df['month'] + shift_value - 1) % 12 + 1


# %%
# Используем метод merge для объединения DataFrame на основе условия
df3 = df2[['address_raw', 'es_code_int','month','cost']].copy()
df3 = df3.groupby(['address_raw', 'es_code_int','month'], as_index=False)['cost'].mean()
merged_df2 = pd.merge(nan_rows_merged_df, df3, on=['address_raw', 'es_code_int','month'], how='left', suffixes=('', '_prev_year'))

# В результате получаем новый DataFrame с добавленными данными
print(nan_rows_merged_df.shape, df2.shape)
print(merged_df2.columns, '\n',merged_df2.shape)

# %%
nan_rows_merged_df2 = merged_df2[merged_df2['cost_prev_year'].isna()]
nan_rows_merged_df2.shape


# %%
merged_df2 = merged_df2.dropna(subset=['cost_prev_year'])
merged_df2.shape

# %%
nan_rows_merged_df2.drop(columns=['cost_prev_year'], inplace=True)
shift_value = -2
nan_rows_merged_df2['month'] = (nan_rows_merged_df2['month'] + shift_value - 1) % 12 + 1


# %%
# Используем метод merge для объединения DataFrame на основе условия
df3 = df2[['address_raw', 'es_code_int','month','cost']].copy()
df3 = df3.groupby(['address_raw', 'es_code_int','month'], as_index=False)['cost'].mean()
merged_df3 = pd.merge(nan_rows_merged_df2, df3, on=['address_raw', 'es_code_int','month'], how='left', suffixes=('', '_prev_year'))

# В результате получаем новый DataFrame с добавленными данными
print(nan_rows_merged_df2.shape, df3.shape)
print(merged_df3.columns, '\n',merged_df3.shape)

# %%
nan_rows_merged_df3 = merged_df3[merged_df3['cost_prev_year'].isna()]
nan_rows_merged_df3.shape

# %%
merged_df3 = merged_df3.dropna(subset=['cost_prev_year'])
merged_df3.shape

# %% [markdown]
# ### fill NaN by adress similarity
# 

# %%
for i, row1 in nan_rows_merged_df3.iterrows():
    matching_rows_df2 = df2[(df2['month'] == row1['month']) & (df2['es_code_int'] == row1['es_code_int'])]

    best_match_index = -1
    best_score = -1

    for j, row2 in matching_rows_df2.iterrows():
        score = spec_match(str(row1['test']), str(row2['test']))
        if score > best_score:
            best_score = score
            best_match_index = j

    if best_match_index != -1:
        nan_rows_merged_df3.at[i, 'prev_year_cost'] = df2.at[best_match_index, 'cost']

# %%
nan_rows_merged_df3['cost_prev_year'] = nan_rows_merged_df3['cost_prev_year'].fillna(nan_rows_merged_df3['prev_year_cost'])
nan_rows_merged_df3.drop(columns=['prev_year_cost'], inplace=True)

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %% [markdown]
# ## mrg_df

# %%
mrg_df = pd.concat([merged_df, merged_df2, merged_df3, nan_rows_merged_df3], ignore_index=True)
mrg_df

# %% [markdown]
# ### сейчас добавми дополнительные данные

# %%
add_info_file = './data3/qart/merget_tr_q2y_2021.xlsx'

# %%
add_df = pd.read_excel(add_info_file)

# %%
add_df.isnull().sum()

# %%
selected_columns = ['TR_object_name', 'TR_planned_cost', 'TR_cost']

# Заполняем пропущенные значения в выбранных колонках нулями
add_df[selected_columns] = add_df[selected_columns].fillna(0)

# %%
mrg_df_bkp = mrg_df.copy()
add_df_bkp = add_df.copy()

# %%
cols_to_copy = ['com_sq_estate_q1',
       'com_sq_building_q1', 'busy_cb_1_q1', 'not_busy_cb_1_q1',
       'rent_out_1_q1', 'rented_1_q1', 'rent_out_sub_1_q1', 'transfer_1_q1',
       'transfer_2_q1', 'busy_cb_2_q1', 'not_busy_cb_2_q1', 'rent_out_2_q1',
       'rented_2_q1', 'rent_out_sub_2_q1', 'transfer_3_q1', 'transfer_4_q1',
       'balance_cost_q1', 'over_price_q1', 'accrual_amount_q1',
       'residual_value_q1', 'technical_condition_q1', 'otdel',
       'years_holding_q1', 'years_before_q1', 'com_sq_estate_q2',
       'com_sq_building_q2', 'busy_cb_1_q2', 'not_busy_cb_1_q2',
       'rent_out_1_q2', 'rented_1_q2', 'rent_out_sub_1_q2', 'transfer_1_q2',
       'transfer_2_q2', 'busy_cb_2_q2', 'not_busy_cb_2_q2', 'rent_out_2_q2',
       'rented_2_q2', 'rent_out_sub_2_q2', 'transfer_3_q2', 'transfer_4_q2',
       'balance_cost_q2', 'over_price_q2', 'accrual_amount_q2',
       'residual_value_q2', 'technical_condition_q2', 'years_holding_q2',
       'years_before_q2', 'com_sq_estate_q3', 'com_sq_building_q3',
       'busy_cb_1_q3', 'not_busy_cb_1_q3', 'rent_out_1_q3', 'rented_1_q3',
       'rent_out_sub_1_q3', 'transfer_1_q3', 'transfer_2_q3', 'busy_cb_2_q3',
       'not_busy_cb_2_q3', 'rent_out_2_q3', 'rented_2_q3', 'rent_out_sub_2_q3',
       'transfer_3_q3', 'transfer_4_q3', 'balance_cost_q3', 'over_price_q3',
       'accrual_amount_q3', 'residual_value_q3', 'technical_condition_q3',
       'years_holding_q3', 'years_before_q3', 'com_sq_estate_q4',
       'com_sq_building_q4', 'busy_cb_1_q4', 'not_busy_cb_1_q4',
       'rent_out_1_q4', 'rented_1_q4', 'rent_out_sub_1_q4', 'transfer_1_q4',
       'transfer_2_q4', 'busy_cb_2_q4', 'not_busy_cb_2_q4', 'rent_out_2_q4',
       'rented_2_q4', 'rent_out_sub_2_q4', 'transfer_3_q4', 'transfer_4_q4',
       'balance_cost_q4', 'over_price_q4', 'accrual_amount_q4',
       'residual_value_q4', 'technical_condition_q4', 'years_holding_q4',
       'years_before_q4', 'TR_object_name', 'TR_planned_cost',
       'TR_cost'] #without 'address_new' 'cad_code', 'build_date', 'balance_accept_date'


# %%
mrg_df

# %%
mrg_df.loc[:, cols_to_copy] = None

# Создание матрицы оценок совпадения
scores_matrix = pd.DataFrame(index=mrg_df.index, columns=add_df.index)

for i, row1 in mrg_df.iterrows():
    for j, row2 in add_df.iterrows():
        scores_matrix.at[i, j] = spec_match(str(row1['test']), str(row2['address_new']))

# Получение индексов максимальных значений для каждой строки
best_matches_indices = scores_matrix.idxmax(axis=1)

# Заполнение колонок в df1
for i, column in enumerate(cols_to_copy):
    mrg_df[column] = add_df.loc[best_matches_indices, column].values


# %%
mrg_df.shape


# %%
mrg_df.to_excel('./data/dataset2021-2022.xlsx', index=False)

# %%


# %%


# %%
print(mrg_df.isna().value_counts())


