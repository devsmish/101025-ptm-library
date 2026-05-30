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
from library.models.category import Category


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
categories = [
    Category(name='Детективы'),
    Category(name='Биографии'),
    Category(name='Поэзия'),
    Category(name='Учебники'),
    Category(name='Справочники')
]

Category.objects.bulk_create(categories)

# Variant 2
names = ['Детективы', 'Биографии', 'Поэзия', 'Учебники', 'Справочники']
categories = [Category(name=name) for name in names]

Category.objects.bulk_create(categories)

"""## Задача 8: Массовое обновление членов библиотеки
**ТЗ:**
1. Найти всех членов библиотеки с ролью 'lib_member'
2. Массово обновить их статус active на True
3. Использовать bulk_update для оптимизации"""
upd_users = User.objects.filter(role='lib_member')

# Меняем статус в памяти
for user in upd_users:
    user.is_active = True

# Массово обновляем в базе данных одним запросом
User.objects.bulk_update(upd_users, fields=['is_active'])

"""## Задача 9: Поиск книг с complex lookups и сортировка
**ТЗ:**
1. Найти книги, название которых содержит слово 'The' (регистронезависимо)
2. Исключить книги с количеством страниц меньше 200
3. Найти книги, опубликованные в определенном диапазоне дат
4. Отсортировать по количеству страниц (по убыванию)"""
books = Book.objects.filter(name__icontains='The', published_date__range=('2002-02-11', '2005-10-07')).\
    exclude(pages__lt=200).order_by('-pages')

# My Variant
"""## Задача 10: Сложные фильтры с Q-объектами
**ТЗ:**
1. Найти авторов, которые либо имеют рейтинг выше 9.0, либо родились до 1980 года
2. Среди найденных авторов взять только активных
3. Исключить авторов без указанной даты рождения
4. Подсчитать общее количество и проверить существование"""
authors = (Author.objects.filter(Q(rating__gt=9.0) | Q(date_of_birth__lt='1980-01-01')).
           filter(deleted=False).exclude(date_of_birth__isnull=True))

authors_count = authors.count()
authors_exist = authors.exists()

print(f"Количество: {authors_count}, Существуют ли: {authors_exist}")

# Lesson Variant
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

"""## Задача 13: Массовое обновление статуса займов
**ТЗ:**
1. Найти все займы с return_date до 2022-01-01 включительно
2. Среди них найти те, которые еще не помечены как возвращенные
3. Массово обновить их статус is_returned на True
4. Подсчитать количество обновленных записей"""
borrows = Borrow.objects.filter(return_actual_date__lt='2022-01-01').filter(is_returned=False)

updated_count = len(borrows)

for borrow in borrows:
    borrow.is_returned = True

Borrow.objects.bulk_update(borrows, fields=['is_returned'])
print(f"Обновлено записей: {updated_count}")

"""## Задача 14: Создание записей займов с валидацией
**ТЗ:**
1. Найти члена библиотеки с id=5
2. Найти книгу с id=25
3. Найти библиотеку с id=1
4. Создать новый заем (Borrow) с датой займа сегодня и датой возврата через 30 дней
5. Проверить, что запись была создана и получить ее id"""
user = User.objects.get(id=5)
book = Book.objects.get(id=25)
library = Library.objects.get(id=1)
borrow = Borrow.objects.create(
    member = user,
    book = book,
    library = library,
    issue_date = timezone.now(),
    return_plane_date = '2026-06-29',
    is_returned = False
)

if borrow:
    print(f"Запись успешно создана!")
else:
    print("Запись не создана.")

"""## Задача 15: Поиск библиотек с фильтрацией по местоположению
**ТЗ:**
1. Найти все библиотеки, в названии которых есть слово "Central" (регистронезависимо)
2. Найти библиотеки, расположенные в городах, содержащих "New" в адресе
3. Объединить результаты с помощью Q-объектов
4. Исключить библиотеки без веб-сайта"""
libraries = (Library.objects.filter(Q(name__icontains="Central") | Q (location__contains="New")).
             exclude(website__isnull=True))


"""## Задача 16: Сложная фильтрация авторов по активности и рейтингу
**ТЗ:**
1. Найти активных авторов с рейтингом от 8.0 до 9.5 включительно
2. Среди них найти тех, кто родился в XX веке (1901-2000 годы)
3. Исключить авторов без указанной даты рождения
4. Получить только первые 10 результатов"""
authors = Author.objects.filter(deleted=False, rating__range=(8.0, 9.5), date_of_birth__year__range=(1901, 2000))[:10]

"""## Задача 17: Создание и поиск категорий с проверкой дубликатов
**ТЗ:**
1. Проверить, существует ли категория с названием "Фантастика"
2. Если не существует - создать новую категорию
3. Если существует - получить существующую категорию
4. Вывести информацию о категории и количестве связанных книг"""
is_exist = Category.objects.filter(name="Фантастика").exists()
if not is_exist:
    category = Category.objects.create(name="Фантастика")
else:
    category = Category.objects.get(name="Фантастика")

books_count = Book.objects.filter(category=category).count()

print(f"Категория: {category.name}")
print(f"Количество связанных книг: {books_count}")

"""## Задача 18: Поиск членов библиотеки с множественными условиями
**ТЗ:**
1. Найти членов библиотеки женского пола в возрасте от 25 до 45 лет
2. Среди них найти тех, кто родился в 1990-2000 годах
3. Исключить неактивных членов
4. Отсортировать по имени"""
users_woman = User.objects.filter(
        role=User.Role.lib_member,
        gender=User.Gender.female,
        age__range=(25, 45),
        birth_date__year__range=(1990, 2000)
    ).exclude(
        is_active=False
    ).order_by('first_name')


"""## Задача 19: Массовое создание связей членов библиотеки с библиотекой
**ТЗ:**
1. Найти всех членов библиотеки с ролью 'lib_member'
2. Найти библиотеку с id=1
3. Создать массово связи M2M между этими членами и библиотекой
4. Исключить членов, которые уже связаны с этой библиотекой"""
library = Library.objects.get(id=1)

users_to_add = User.objects.filter(
    role=User.Role.lib_member
).exclude(
    membership_records__library=library
)

new_memberships = [
    Membership(member=user, library=library)
    for user in users_to_add
]

if new_memberships:
    Membership.objects.bulk_create(new_memberships)
    print(f"Успешно добавлено новых связей: {len(new_memberships)}")
else:
    print("Все активные читатели уже привязаны к этой библиотеке.")

"""## Задача 20: Сложный поиск займов с временными условиями
**ТЗ:**
1. Найти все займы, сделанные в 2022 году
2. Среди них найти те, которые были возвращены вовремя (до или в дату return_date)
3. Исключить займы без указанной даты возврата
4. Сгруппировать результаты по месяцам и посчитать количество в каждом месяце"""



"""## Задача 21: Поиск книг по связанным моделям с множественными условиями
**ТЗ:**
1. Найти все книги, написанные авторами с рейтингом выше 7.5
2. Среди них найти те, которые опубликованы пользователями с ролью 'admin' или 'employee'
3. Исключить книги без автора и без издателя
4. Отсортировать по дате публикации (новые первыми)"""




"""## Задача 22: Создание постов с валидацией и связями
**ТЗ:**
1. Найти активного автора с наивысшим рейтингом
2. Создать для него 3 поста с разными заголовками
3. Проверить, что все посты были созданы успешно"""



"""## Задача 23: Сложная фильтрация займов по датам и статусам
**ТЗ:**
1. Найти займы, сделанные в последние 6 месяцев от текущей даты
2. Среди них найти те, которые должны были быть возвращены более 30 дней назад
3. Получить информацию о библиотеке и пользователе для каждого займа"""


"""## Задача 24: Массовое обновление авторов с условной логикой
**ТЗ:**
1. Найти всех авторов без указанной даты рождения
2. Найти авторов с рейтингом ниже 5.0
3. Объединить эти группы с помощью Q-объектов
4. Массово установить им рейтинг 5.0 и статус is_active=False"""



"""## Задача 25: Поиск членов библиотеки по активности в библиотеках
**ТЗ:**
1. Найти всех членов библиотеки, которые связаны с более чем одной библиотекой
2. Среди них найти тех, кто имеет активные займы (не возвращенные)
3. Исключить членов с ролью 'admin', 'staff'
4. Отсортировать по фамилии и имени"""



"""## Задача 26: Создание связей между книгами и библиотеками
**ТЗ:**
1. Найти все книги жанра 'SCIENCE_FICTION'
2. Найти библиотеки, в названии которых есть слово "Tech"
3. Создать связи many-to-many между этими книгами и библиотеками
4. Проверить, что связи были созданы"""


"""## Задача 27: Анализ займов по временным периодам
**ТЗ:**
1. Найти все займы за 2023 год
2. Разделить их на кварталы (Q1: янв-март, Q2: апр-июнь, Q3: июль-сен, Q4: окт-дек)
3. Для каждого квартала посчитать количество займов и возвратов
4. Найти квартал с наибольшей активностью"""



"""## Задача 28: Поиск и создание категорий с иерархией
**ТЗ:**
1. Проверить существование категорий: "Классическая литература", "Современная проза", "Детская литература"
2. Создать отсутствующие категории
3. Найти книги без категории и присвоить им категорию "Без категории"
4. Вывести статистику по количеству книг в каждой категории"""



"""## Задача 29: Сложный поиск с множественными связями
**ТЗ:**
1. Найти членов библиотеки, которые связаны с библиотеками с веб-сайтом
2. Среди них найти тех, кто брал книги автора с рейтингом выше 8.0
3. Исключить членов младше 21 года
4. Получить уникальный список таких членов"""



"""## Задача 30: Комплексная работа с датами и статусами
**ТЗ:**
1. Найти все займы, которые были сделаны в выходные дни (суббота/воскресенье)
2. Среди них найти те, которые длились более 45 дней
3. Проверить статус возврата и подсчитать просроченные
4. Создать отчет по библиотекам с наибольшим количеством проблемных займов"""
