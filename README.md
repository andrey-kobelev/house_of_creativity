# Дом творческих 

> Дом творческих — это дом для творческих людей. Это — сообщество людей, для которых нет грани между ведением блога и дружбой в социальных сетях.
> 
> Дружба и рассказы о новых, неизведанных впечатлениях — вот что вы найдете на нашем ресурсе. Миллионы блогов по различным темам. Путешествия, политика, развлечения, мода, литература, дизайн и все другие сферы человеческой деятельности.
> 
> Творчество, разнообразие и свобода взглядов и самовыражения — основные черты наших пользователей.

## Как развернуть проект локально

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/andrey-kobelev/house_of_creativity.git
```

```
cd house_of_creativity
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env  
```

```
source env/bin/activate  
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip  
```

```
pip install -r requirements.txt  
```

Выполнить миграции:

```
python3 manage.py migrate  
```

Запустить проект:

```
python3 manage.py runserver  
```

