#encoding:utf8
from collections import OrderedDict, defaultdict
from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError,\
    ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils import timezone
import traceback
import datetime


class Student(models.Model):
    CONTRACT_CHOICES = (
                        ('B',u'Бюджет'),
                        ('I',u'Контракт индивидуал.'),
                        ('C',u'Контракт фирма'),
                       )

    PROGRAM_STATUS_CHOICES = (
                              ('D',u'Довузовая подготовка'),
                              ('B',u'Бакалавриат'),
                              ('M',u'Магистратура'),
                              ('A',u'Аспирантура'),
                              ('Q',u'Докторантура'),
                              ('P',u'Стажировка'),
                              ('S',u'Краткосрочная программа'),
                              )

    SEX_CHOICES = (
                   ('F',u'Ж'),
                   ('M',u'М'),
                   )

    PRE_TRAINING_CHOICES = (
                            ('1S',u'Подготовка к 1 СУ'),
                            ('1SM',u' Подготовка к 1 СУ с модулем'),
                            )

    last_name = models.CharField(u"Фамилия", max_length=255)
    first_name = models.CharField(u"Имя", max_length=255)

    last_name_lat = models.CharField(u"Фамилия (лат.)", max_length=255)
    first_name_lat = models.CharField(u"Имя (лат.)", max_length=255)

    sex = models.CharField(u"Пол", max_length = 1, choices = SEX_CHOICES)

    birth_date = models.DateField(u'Дата рождения', null = True)

    citizenship = models.CharField(u"Гражданство", max_length = 255)
    passport_num = models.CharField(u"Номер паспорта", max_length = 255)
    passport_duration_from_date = models.DateField(u"Паспорт выдан", null = True)
    passport_duration_till_date = models.DateField(u"Паспорт истекает", null = True)

    visa_number = models.CharField(u"Номер визы", max_length = 50)
    visa_delivery_date = models.DateField(u"Дата выдачи визы", null = True)
    visa_entrance_from_date = models.DateField(u"Въезд с", null = True)
    visa_entrance_till_date = models.DateField(u"Въезд до", null = True)
    visa_id_num = models.CharField(u"Идентиф. №", max_length = 50)

    migration_number = models.CharField(u"Номер миграционной карты", max_length = 50)
    migration_date = models.DateField(u"Дата посл. перес. гр.", null = True)
    migration_border = models.CharField(u"Пункт пересечения", max_length = 50)
    migration_uvd = models.CharField(u"УВД", max_length = 50)
    migration_from_date = models.DateField(u"Мигр. регистр. с", null = True)
    migration_till_date = models.DateField(u"Мигр. регистр. до", null = True)

    invitation_sent_date = models.DateField(u"Приглашение отдано в ОПК", null = True)
    invitation_received_date = models.DateField(u"Приглашение получено из ОПК", null = True)
    invitation_number = models.CharField(u"№ приглашения", max_length = 100)
    invitation_duration_from_date = models.DateField(u"Приглашение действительно с", null = True)
    invitation_duration_till_date = models.DateField(u"Приглашение действительно до", null = True)

    pay_registration_fee_date = models.DateField(u"Оплата регистрационного взноса", null = True)
    pay_invitation_fee_date = models.DateField(u"Оплата приглашения", null = True)

    contract_status = models.CharField(u"Статус", max_length = 1, choices = CONTRACT_CHOICES) # state-paid or contract
    contract_number = models.CharField(u"Контракт", max_length = 100)
    contract_date = models.DateField(u"Дата контракта", null = True)
    #contract_company_name = models.CharField(u"Название фирмы", max_length = 100)
    contract_company_name = models.ForeignKey('Firm', null = True, verbose_name = u"Название фирмы")
    order_number = models.CharField(u"Приказ", max_length = 100)
    order_date = models.DateField(u"Дата приказа", null = True)

    program_status = models.CharField(u"Программа обучения", max_length = 1, choices = PROGRAM_STATUS_CHOICES)
    #faculty_name = models.CharField(u"Название института", max_length = 200)
    faculty_name = models.ForeignKey('Institute', null = True, verbose_name = u"Название института")
    faculty_grade = models.CharField(u"Курс", max_length = 20)
    study_from_date = models.DateField(u"Обучение с", null = True)
    study_till_date = models.DateField(u"Обучение до", null = True)
    study_group_number = models.CharField(u"Номер группы", max_length = 50)
    pre_univ_training = models.CharField(u"Довузовская подготовка", max_length = 5, choices = PRE_TRAINING_CHOICES)
    program_change = models.CharField(u"Смена программы обучения", max_length = 255)
    case_omir_transfer = models.BooleanField(u"Передача личного дела из ОМиР")
    case_ok_receive = models.BooleanField(u"Получено личное дело в ОК")
    case_ok_sent = models.BooleanField(u"Личное дело передано в УО")

    pre_arrival_date_char = models.CharField(u"Ожидаемое прибытие", max_length = 50)
    pre_arrival_date_check = models.BooleanField(u"Прибытие принято")
    arrival_date = models.DateField(u"Дата прибытия",null=True)

    phone = models.CharField(u"Тел. номер", max_length = 50)
    e_mail = models.CharField(u"e-mail", max_length = 255)
    note = models.TextField(u"Примечание:")
    note_omir = models.TextField(u"Примечание(только ОМиР):")
    register_date = models.DateField(u"Дата регистрации", null = True)

    address = models.CharField(u"Адрес проживания", max_length = 511)
    address_migration = models.CharField(u"Адрес мигр. уч.", max_length = 511)
    address_native = models.CharField(u"Адрес на родине", max_length = 511)

    @classmethod
    def get_fields(cls, perm):
        new_dic = OrderedDict()
        fields = [f for f in Student._meta.fields if not f.name in ('id', 'studentrecordlock') and f.name in perm]
        for f in fields:
            new_dic[f.name] = f
        return new_dic

    def get_dict(self, perm):
        new_dic = OrderedDict()
        fields = self.get_fields(perm)

        for field in fields.values():
            display_attr = 'get_{}_display'.format(field.name)
            if hasattr(self, display_attr):
                val = getattr(self, display_attr)()
            else:
                val = getattr(self, field.name)

            if hasattr(val, 'strftime'):
                val = val.strftime('%d.%m.%Y')

            if isinstance(val, models.Model):
                val = val.name

            new_dic[field.name] = (field.verbose_name, val or '-')
        return new_dic

    def save(self, *args, **kwargs):
        ''' Creates lock automatically '''
        is_new = not self.pk
        super(Student, self).save(*args, **kwargs)
        if is_new:
            StudentRecordLock.objects.create(record = self, locked_date = timezone.now())
        else:
            #unlock student after editing
            lock = self.studentrecordlock
            lock.version += 1
            lock.save()
            #lock.unlock()

    def __unicode__(self):
        return self.first_name+" "+self.last_name

    @classmethod
    def get_table_header(cls, perm = set()):
        fields = cls.get_fields(perm).values()
        headline = [f.verbose_name for f in fields]
        return headline

Student.crit_cases = OrderedDict()

def crit_case(name):
    def wrapper(func):
        func.name = name
        Student.crit_cases[func.func_name]=func
        return func
    return wrapper

@crit_case(u"ОПК")
def get_opk_late():
    return Student.objects.filter(invitation_sent_date__lte = datetime.date.today())

@crit_case(u"Пригл.")
def get_inv_late():
    return Student.objects.filter(invitation_duration_till_date__lte = datetime.date.today()+datetime.timedelta(days=30))


class StudentRecordLock(models.Model):
    record = models.OneToOneField(Student, primary_key = True)
    locked_date = models.DateTimeField(null = True)
    locked_by = models.ForeignKey(User, null = True)
    version = models.IntegerField(default = 0)

    lock_timeout = timedelta(minutes = 2)
    @classmethod
    def check_timeout(cls):
        cls.objects.filter(locked_date__lte = timezone.now() - cls.lock_timeout).update(locked_by = None)

    def lock(self, user):
        print "WARNING LOCK"
        traceback.print_stack()
        return
        '''
        self.check_timeout()
        # Try to lock this record. We can lock it if it isn't locked or if it is locked by same user
        return type(self).objects.filter(
                                         Q(pk = self.pk) & (
                                            Q(locked_by = None) |
                                            Q(locked_by = user))
                                         ).update(locked_date = timezone.now(),
                                                  locked_by = user)
        '''

    def unlock(self, user=None):
        print "WARNING UNLOCK"
        traceback.print_stack()
        return
        '''
        query = type(self).objects.filter(pk = self.pk)
        if user:
            query = query.filter(locked_by = user)
        query.update(locked_by = None)
        '''


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class GroupPermission(models.Model):
    field_name = models.CharField(max_length=300)
    permission = models.CharField(max_length=3) #RW
    group = models.ForeignKey(Group)

    @classmethod
    def permissions(cls, group):
        perm = {}
        for p in group.grouppermission_set.all():
            perm[p.field_name] = set(p.permission)
        return perm

    def validate_unique(self,  *args, **kw):
        super(GroupPermission, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(field_name = self.field_name).filter(group = self.group).exists():
            raise ValidationError(
                {
                    NON_FIELD_ERRORS:
                    ('This permission already exists.',)
                }
            )


def user_permissions(user, access = None):
    ''' If access is set returns set of fields
    otherwise returns dict {field:set('R','W')}
    '''
    #TODO: Optimize with index and join
    perm = defaultdict(set)
    for g in user.groups.all():
        for name, p in GroupPermission.permissions(g).items():
            perm[name] |= p
    if access:
        return {name for name, p in perm.items() if set(access) <= p}
    return perm


class Institute(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Firm(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
