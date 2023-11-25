# %% [markdown]
# ## prep address
# 
# 

# %%
import os
import pandas as pd

# %% [markdown]
# ### tmp

# %%
def remove_value(row, remove_this_col_num, remove_from_this_col_num, additional_str_value=''):
    r = row[remove_from_this_col_num].replace(additional_str_value+str(row[remove_this_col_num]), '')
    return r

def remove_str(row, remove_from_this_col_num, str_value=''):
    return row[remove_from_this_col_num].replace(str_value, '')
def truncate_to_first_letter(input_string):
    for index, char in enumerate(input_string):
        if char.isalpha():
            return input_string[index:]
    # If there are no letters in the string, return the original string
    return ''
def cleanup_address(ddd):
    ddd = ddd.dropna(subset=[0], how='all')
    ddd1 = ddd[ddd.iloc[:, [3, 8, 11]].isna().all(axis=1)]
    ddd2 = ddd1[ddd1[0].apply(lambda x: str(x).startswith("Итого по направлению"))]
    ddd3 = ddd2[~ddd2[7].astype(str).str.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
    ddd4 = ddd3[~ddd3[7].astype(str).str.contains('прошлого года', case=False)]
    ddd4 = ddd4[~ddd4[7].astype(str).str.contains('прошлых', case=False)]
    ddd4[7] = ddd4[7].str.lower()
    ddd4[6] = ddd4[6].str.lower()
    ddd4[12] = ddd4[7].copy()


    ddd5 = ddd4.copy()
    ddd5[7] = ddd5.apply(remove_value, remove_this_col_num=4, remove_from_this_col_num=7, additional_str_value='ст.', axis=1)
    ddd5[7] = ddd5.apply(remove_value, remove_this_col_num=4, remove_from_this_col_num=7, additional_str_value='ст. ', axis=1)
    ddd6 = ddd5.copy()
    ddd6[7] = ddd5.apply(remove_str, remove_from_this_col_num=7, str_value='другие расходы.', axis=1)
    ddd10 = ddd6.copy()
    stoplist = [
        'оплата потребления электроэнергии',
        'оплата потребления тепловой энергии',
        'горячее водоснабжение',
        'затраты на ',
        'оплата водоотведения',
        'холодное водоснабжение ',
        'оплата холодного водоснабжения',
        'оплата горячего водоснабжения',
        'оплата водоснабжения',
        'канализации',
        'горячая вода',
        'холодная вода',
        'оплата за',
        'прошлого года',
        'водоснабжения','водоотведения','водоотведение','водоснабжение','электроэнергии', 'горячее','горячего','вода','затраты на', 'холодного','холодное','горячая','холодная','энергии', 'оплата', '.оплата',
        'канализацию ', 'канализация ',
        'потребления','потребление','тепловой','газа', 'электроэнерги',
        'тепловую энергию по тарифам ',
        'по тарифам', 'тепловую энергию',
        'дизельное топливо', 'эектроэнергию ',
        'по тприфам', 'оплат за', 'обслуживание (услуги)',
        'плата за технологическое присоединение к электрическим сетям', 'плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом г.ленск ст. 134.1100',
        'расходы по оплате', 'расходы по приобретению', 'дизельного', 'топлива', 'отопление',
    ]
    for w in stoplist:
        ddd10[7] = ddd10.apply(remove_str, remove_from_this_col_num=7, str_value=w, axis=1)
    import re
    rem = []


    ddd10[7] = ddd10.apply(remove_value, remove_this_col_num=4, remove_from_this_col_num=7, axis=1)
    stoplist = [
        'оплата потребления электроэнергии',
        'оплата потребления тепловой энергии',
        'горячее водоснабжение',
        'затраты на ',
        'оплата водоотведения',
        'холодное водоснабжение ',
        'оплата холодного водоснабжения',
        'оплата горячего водоснабжения',
        'оплата водоснабжения',
        'канализации',
        'горячая вода',
        'холодная вода',
        'оплата за',
        'водоснабжения','водоотведения','водоотведение','водоснабжение','электроэнергии', 'горячее','горячего','вода','затраты на', 'холодного','холодное','горячая','холодная','энергии', 'оплата', '.оплата',
        'канализацию ', 'канализация ',
        'потребления','потребление','тепловой','газа', 'электроэнерги',
        'тепловую энергию по тарифам ',
        'по тарифам', 'тепловую энергию',
        'дизельное топливо', 'эектроэнергию ',
        'по тприфам', 'оплат за', 'обслуживание (услуги)',
        'плата за технологическое присоединение к электрическим сетям', 'плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом г.ленск ст. 134.1100',
        'расходы по оплате', 'расходы по приобретению', 'дизельного', 'топлива', 'отопление',
        'зо .01','зо .02','зо .03','зо .04','зо .010000','зо .020000','зо .030000','зо .040000',
        'зо зо.','зо ','134,1000,02','плата за сброс сточных вод', 'услуги',
        "дгу.  здание", "дгу.  ю",
        "дгу. плата за негативное воздействие на централ.систему"
    ]
    for w in stoplist:
        ddd10[7] = ddd10.apply(remove_str, remove_from_this_col_num=7, str_value=w, axis=1)
    print(rem)
    ddd10[7] = ddd10[7].apply(truncate_to_first_letter)
    ddd10.columns
    ddd10.columns = ['0','year', 'smeta_otdeleniya', '3', 'expens_type_code', '5', 'expense_type_name', 'address', '8', 'cost', 'cost2_same', '11', 'address_raw']
    return ddd10

# %% [markdown]
# ### prepare data

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
# Указать путь к папке, содержащей файлы .xlsx
folder_path = './raw_data/train_data/Expenses'

# Список для хранения pandas DataFrame
dataframes = []

# Чтение файлов .xlsx в указанной папке
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx') and file_name.startswith(('1', '2')):
        file_path = os.path.join(folder_path, file_name)
        print(file_name)
        # Чтение файла в DataFrame
        df = pd.read_excel(file_path, header=None)
        df[11] = pd.to_datetime(df[11], errors='coerce')
        df.dropna(subset=[11], inplace=True)
        df.reset_index(drop=True, inplace=True)
        # Добавление DataFrame в список
        
        df[11] = pd.to_datetime(df[11])
        df['formatted_date'] = df[11].dt.strftime('%m.%Y')
        df.drop(columns=[0,1,5,8,10], inplace=True)
        df.columns = ['smeta','distr', 'code','code_discription','address_raw','cost','full_date','data_short' ]
        df = df.replace(r'\s+',' ',regex=True)
        df['es_code_int'] = df.apply(get_type_of_es, axis=1)
        df.to_excel('./data/'+file_name, index=False)



# %%
def remove_value(row, remove_this_col_num, remove_from_this_col_num, additional_str_value=''):
    r = row[remove_from_this_col_num].replace(additional_str_value+str(row[remove_this_col_num]), '')
    return r

# %%
def to_lower(listin):
    return [str(element).lower() for element in listin]

citys = pd.read_excel('./extra/np-dvfo.xlsx', header=None)[0].to_list()
streets = pd.read_excel('./extra/names-dvfo.xlsx', header=None)[0].to_list()
numbers = [str(i) for i in range(1, 1000)]
citys = to_lower(citys)
streets = to_lower(streets)
numbers = to_lower(numbers)


# %%
import re
folder_path = './data/'
# Чтение файлов .xlsx в указанной папке
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx') and file_name.startswith(('1', '2')):
        file_path = os.path.join(folder_path, file_name)
        
        # Чтение файла в DataFrame
        df = pd.read_excel(file_path)
        df['address_clean'] = df.apply(remove_value, remove_this_col_num='code', remove_from_this_col_num='address_raw', additional_str_value='ст. ', axis=1)
        df['address_clean'] = df.apply(remove_value, remove_this_col_num='code', remove_from_this_col_num='address_clean', additional_str_value='ст.', axis=1)
        df['address_clean'] = df.apply(remove_value, remove_this_col_num='code', remove_from_this_col_num='address_clean', axis=1)
        df['address_clean'] = df['address_clean'].str.lower()
        stoplist = [
        'оплата потребления электроэнергии',
        'оплата потребления тепловой энергии',
        'горячее водоснабжение',
        'затраты на ',
        'оплата водоотведения',
        'холодное водоснабжение ',
        'оплата холодного водоснабжения',
        'оплата горячего водоснабжения',
        'оплата водоснабжения',
        'канализации',
        'горячая вода',
        'холодная вода',
        'оплата за',
        'прошлого года',
        'водоснабжения','водоотведения','водоотведение','водоснабжение','электроэнергии', 'горячее','горячего','вода','затраты на', 'холодного','холодное','горячая','холодная','энергии', 'оплата', '.оплата',
        'канализацию ', 'канализация ',
        'потребления','потребление','тепловой','газа', 'электроэнерги',
        'тепловую энергию по тарифам ',
        'по тарифам', 'тепловую энергию',
        'дизельное топливо', 'эектроэнергию ',
        'по тприфам', 'оплат за', 'обслуживание (услуги)',
        'плата за технологическое присоединение к электрическим сетям', 'плата за технологическое присоединение к электрическим сетям (в случаях, не связанным со строительством,реконстр. и кап.ремонтом г.ленск ст. 134.1100',
        'расходы по оплате', 'расходы по приобретению', 'дизельного', 'топлива', 'отопление',
    ]
        for w in stoplist:
            df['address_clean'] = df.apply(remove_str, remove_from_this_col_num='address_clean', str_value=w, axis=1)
        df['test']=df['address_clean']
        #df['test2']=df['col2'].str[-30:] +df['address_clean']
        df['test'] = df['test'].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))

        # Шаг 2: Оставить только слова и последовательности цифр не длинее 3 знаков подряд
        #df['test'] = df['test'].apply(lambda x: re.sub(r'\b(?:\d{1,3}|\w{1,})\b', ' ', x))

        # Шаг 3: Оставить только те слова, которые лежат в одном из двух списков: cities, streets
        df['test'] = df['test'].apply(lambda x: ' '.join(word for word in x.split() if word in citys or word in streets or word in numbers))
        df.to_excel('./data3/es/'+file_name, index=False)


