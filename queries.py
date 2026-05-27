import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from library.models.users import User, Membership
from library.models.authors import Author
from library.models.books import Book
from django.db.models import Q
from library.models.library import Library
from django.utils import timezone
from library.models.borrow import Borrow


"""## Задача 1: Создание нового члена библиотеки
1. Создать нового члена библиотеки
2. Установить обязательные поля: email='new_member@test.com', role='lib_member'
3. Добавить дополнительные данные: first_name='John', last_name='Doe', gender='male', age=25, birth_date
4. Сохранить в базе данных"""
# new_user = User.objects.create_user(username='Serg', email='serg@gmail.com', password='qwertyuiop',
#                                     role='lib_member',
#                                     first_name='John',
#                                     last_name='Doe',
#                                     gender='male',
#                                     age=25,
#                                     birth_date='2000-01-22')

"""## Задача 2: Получение конкретного автора и обновление рейтинга **ТЗ:**
1. Найти автора с id=1
2. Обновить его рейтинг на 9.5
3. Сохранить изменения в базе данных"""

# author = Author.objects.filter(id=1).update(rating=9.5)

# author = Author.objects.filter(id=1).first()
# author.rating = 8.5
# author.save()

author = Author.objects.get(id=1)
author.rating = 7.5
author.save()

"""## Задача 3: Фильтрация книг по категории и количеству страниц с подсчетом **ТЗ:**
1. Найти все книги категории с названием, содержащим 'Fiction'
2. Исключить книги с количеством страниц меньше 200
3. Подсчитать количество таких книг"""

books = Book.objects.filter(
    category__name__contains='Fiction',
    pages__gt=200
)
print(books)
print(books.query)
print(books.count())

"""## Задача 4: Поиск членов библиотеки с использованием Q-объектов
**ТЗ:**
1. Найти всех членов библиотеки, которые являются либо администраторами, либо сотрудниками
2. Исключить неактивных членов
3. Отсортировать по фамилии и имени"""

users_staff_members = User.objects.filter(
    Q(role='admin') | Q(role='moderator')
).exclude(is_active=False).order_by('last_name', 'first_name')

for staff_members in users_staff_members:
    print(staff_members)

"""## Задача 5: Поиск авторов с использованием field lookups
**ТЗ:**
1. Найти всех авторов, чье имя начинается с 'A'
2. Найти авторов с рейтингом выше 8.5
3. Найти авторов, родившихся после 1950 года
4. Получить первого автора из результата"""

author = Author.objects.filter(name__startswith='A')

author_rating = Author.objects.filter(rating__gt=8.5)

author_year = Author.objects.filter(date_for_birth__year__gt=1950)

first_author = author.first()

print(author)
print(author_rating)
print(author_year)
print(first_author.name)

"""## Задача 6: ## Массовое создание категорий
**ТЗ:**
1. Создать список из 5 новых категорий одним запросом
2. Категории: 'Детективы', 'Биографии', 'Поэзия', 'Учебники', 'Справочники'
3. Использовать bulk_create для оптимизации"""

"""## Задача 8: Массовое обновление членов библиотеки
**ТЗ:**
1. Найти всех членов библиотеки с ролью 'lib_member'
2. Массово обновить их статус active на True
3. Использовать bulk_update для оптимизации"""

"""## Задача 9: Поиск книг с complex lookups и сортировка
**ТЗ:**
1. Найти книги, название которых содержит слово 'The' (регистронезависимо)
2. Исключить книги с количеством страниц меньше 200
3. Найти книги, опубликованные в определенном диапазоне дат
4. Отсортировать по количеству страниц (по убыванию)"""

"""## Задача 10: Сложные фильтры с Q-объектами
**ТЗ:**
1. Найти авторов, которые либо имеют рейтинг выше 9.0, либо родились до 1980 года
2. Среди найденных авторов взять только активных
3. Исключить авторов без указанной даты рождения
4. Подсчитать общее количество и проверить существование"""

'''## Задача 10: Сложные фильтры с Q-объектами
**ТЗ:**
1. Найти авторов, которые либо имеют рейтинг выше 9.0, либо 
родились до 1980 года
2. Среди найденных авторов взять только активных
3. Исключить авторов без указанной даты рождения
4. Подсчитать общее количество и проверить существование'''

from django.db.models import Q

autors = Author.objects.filter(
    Q(rating__gt=9.0)|Q(date_for_birth__year__lt=1980),
    deleted=False
).exclude(date_for_birth__isnull=True)

print(autors)
print(autors.query)
print(autors.count())
print(autors.exists())

if autors:
    print(autors)

"""## Задача 11: Создание связи члена библиотеки с библиотекой через M2M
**ТЗ:**
1. Найти члена библиотеки с id=15
2. Найти библиотеку с id=2
3. Создать связь many-to-many между членом и библиотекой
4. Проверить, что связь была создана успешно"""

member= User.objects.get(id=15)
lib= Library.objects.get(id=2)
membership= Membership.objects.create(member=member,library=lib)
print(member, membership.library)

"""## Задача 12: Поиск просроченных займов с использованием Q объектов
**ТЗ:**
1. Найти все займы (Borrow), которые не возвращены (is_returned=False)
2. Среди них найти те, где return_date уже прошла (меньше текущей даты)
3. Исключить займы, где return_date равно None
4. Отсортировать по дате займа (старые первыми)"""

date = str(timezone.now().date())
# print(date)
# print(type(date))
borrows = Borrow.objects.filter(
    Q(is_returned=False) & Q(return_plane_date__lt=date)
).exclude(return_actual_date__isnull=True).order_by("issue_date")

print(borrows)

for borrow in borrows:
    print(borrow)
