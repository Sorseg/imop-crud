#coding:utf8
#launch via manage.py
from django.contrib.auth.models import User, Group
from django.db import transaction
from students.models import *
from random import choice
import sys

names = u'''\
Себастьян Sebastian Ветель Vettel
Фернандо Fernando Алонсо Alonso
Кими Kimi Райконен Raikkonnen
Льюис Lewis Хэмильтон Hamilton
Дженсон Jenson Баттон Button
Марк Mark Уэббер Webber
Фелипе Felipe Масса Massa
Роман Romain Грожан Grosjean
Сергио Sergio Перес Perez
Нико Nico Росберг Rosberg
Нико Nico Хюлькенберг Hulkenberg
Камуи Kamui Кобаяши Kobayashi
Михаэль Michael Шумахер Schumacher
Пол Paul ди_Реста di_Resta
Пастор Pastor Мальдонадо Maldonado
Бруно Bruno Сенна Senna
Жан-Эрик Jean-Eric Вернь Vergne
Даниэль Daniel Рикьярдо Ricciardo
Виталий Vitaly Петров Petrov
Тимо Timo Глок Glock
Шарльз Charles Пик Pic
Хейки Heikki Ковалайнен Kovalainen
Жером Jerome д'Амброзио d'Ambrosio
Нараин Narain Картикиян Karthikeyan
Педро Pedro де_ля_Роса de_la_Rosa
Даниил Danil Бубнов Bubnov'''

nms = []
srn = []
for line in names.split('\n'):
    line = [l.replace('_',' ') for l in line.split(' ')]
    #print ' '.join(line), len(line)
    nms.append((line[0],line[1]))
    srn.append((line[2],line[3]))

#print '\n'.join([' '.join(i) for i in nms])
#print '\n'.join([' '.join(i) for i in srn])

citiz = u'Россия Украина Германия Испания Финляндия Великобритания \
Япония Мексика Бельгия Индия Бразилия Австралия Франция Венесуэла'.split()


#Students:
if '-s' in sys.argv:
    Student.objects.all().delete()

    i = 0
    with transaction.commit_on_success():
        while i<500:
            i += 1
            if not i%100:
                print i
            nm = choice(nms)
            sr = choice(srn)
            s = Student(first_name = nm[0],
                        first_name_lat = nm[1],
                        last_name = sr[0],
                        last_name_lat = sr[1],
                        citizenship = choice(citiz),
                        sex = choice(['F','M']))
            s.save()


#Countries:
if '-c' in sys.argv or '-a' in sys.argv:
    import urllib
    try:
        page = urllib.urlopen('http://www.artlebedev.ru/tools/country-list/tab/').read()
    except:
        page = open('countries.txt').read()
    with transaction.commit_on_success():
        for line in page.split('\n'):
            name = line.split('\t')[0]
            if name and not name == 'name':
                Country(name=name).save()

#Permissions:
if any (i in sys.argv for i in ['-p','-a']):
    GroupPermission.objects.all().delete()
    data = open('permissions.txt')
    group = None
    with transaction.commit_on_success():
        #GroupPermission.objects.all().delete()
        for line in data:
            line = line.rstrip()
            if not line:
                continue
            if not (line.startswith('\t') or line.startswith(' ')):
                group = Group.objects.get_or_create(name = line)[0]
            else:
                curr_perm = 'RW'
                f_name = line.strip()
                if len(line.split()) > 1:
                    f_name, curr_perm = line.split()[:2]

                perm = GroupPermission.objects.get_or_create(group_id = group.id, field_name=f_name)[0]
                perm.permission = ''.join(set(curr_perm)|set(perm.permission))
                perm.save()


if all(p not in sys.argv for p in ['-s','-c','-a','-p']):
    print ("-s reset students\n"
           "-c reset countries\n"
           "-p reset permissions\n"
           "-a reset all\n")









