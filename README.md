# Цифровой прорыв. Сезон ИИ. Кейс ЦБ РФ - Оценка эффективности вложений в содержание недвижимости

Команда - **Опять Ботать**

Данный репозиторий содержит код для подготовки данных и код модели по кейсу ЦБ РФ "Оценка эффективности вложений в содержание недвижимости".

Стек: **Python**, **Pandas**

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Лицензия](#лицензия)

## Установка

Для установки и запуска этого проекта вам потребуются следующие зависимости:

**pandas**: версия **2.1.3**

Вы можете установить их с помощью pip, выполнив следующую команду:

```
$ pip install -r requirements.txt
```

Эта команда автоматически установит все необходимые зависимости, указанные в файле [requirements.txt](requirements.txt). Пожалуйста, удостоверьтесь, что у вас установлен **Python3.10** и **pip** перед выполнением этой команды.

После успешной установки зависимостей вы будете готовы использовать и запускать проект.

## Использование

Файлы с кодом в формате Jupiter Notebook:

parser_list_on.ipynb - парсит файли из папки LIST ON

union_q2y.ipynb - конкатенирует файлы полученные с парсера выше

stnd_data.ipynb - стандартизирует файл, созданный парсером выше

merge_data.ipynb - мерджит файл TR-типа из KC_TR_KR и файл полученный из стнадартера выше

kc_tr_kr_operating.ipynb - парсит файлы из KC_TR_KR

prepare.py - подготовка данных

formate_dataset.ipynb - конечное представление данных и обучение модели, а также предикт

Заменить пути к файлам на актуальные, после чего запустить все ячейки.

## Лицензия

Проект лицензирован по лицензии Apache License 2.0 - подробности см. в файле [LICENSE](LICENSE).

Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/