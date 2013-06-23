# -*- coding: utf-8 -*-
import re
import string
import random
import os
from django.conf import settings

def gen_date_dict(prefix, date = None):
    if not date:
        date = ['']*10
    try:
        return {
            prefix+'d_01':date[0],
            prefix+'d_02':date[1],
            prefix+'m_01':date[3],
            prefix+'m_02':date[4],
            prefix+'y_01':date[6],
            prefix+'y_02':date[7],
            prefix+'y_03':date[8],
            prefix+'y_04':date[9]
            }
    except IndexError:
        raise ValueError('corrupted date:'+str(date))

def gen_enum(prefix,string):
    return {prefix+'_{:02}'.format(i):c.encode('cp1251') for i,c in enumerate(string,1)}


CHESS_KEYS = [r'fname_\d\d',#
              r'lname_\d\d',#
              r'cntry_\d\d',#
              r'bd[dmy]_\d\d',#
              r'sex_[mf]',#
              r'passser_\d\d',#
              r'passno_\d\d',#
              r'passgot[dmy]_\d\d',#
              r'passt[dmy]_\d\d',#
              r'visadel[dmy]_\d\d',#
              r'vst[dmy]_\d\d',#
              r'mgrd[dmy]_\d\d',
              r'mgrt[dmy]_\d\d',
              r'mgr[sna]_\d\d',
              r'visaser_\d\d',
              r'visanum_\d\d']



CHESS_PATTERN = re.compile('(' + '|'.join(CHESS_KEYS) + r')')


def render(doc, data):
    doc_fname = os.path.basename(doc)
    contents = open(os.path.join(settings.DOCS_ROOT, doc_fname.encode('utf8'))).read()
    if doc == u'Уведомление.rtf':
        uv_replace = gen_chess_data(data)
        result = CHESS_PATTERN.sub(lambda x:uv_replace.get(x.group(),''), contents)
        return result


def gen_chess_data(data):
    result = {}

    def get_val(key):
        val = data.get(key, ('', ''))[1].upper()
        return '' if val == '-' else val

    def update_enum(key, pref):
        result.update(gen_enum(pref, get_val(key)))

    def update_date(key,pref):
        result.update(gen_date_dict(pref,get_val(key)))

    def split_num(string):
        digits = [c for c in string if c.isdigit()]
        return digits[:4], digits[4:]


    #WARNING!!!! fname and lname are swapped in file
    update_enum('first_name','lname')
    update_enum('last_name','fname')
    update_enum('citizenship','cntry')
    update_date('birth_date','bd')
    sex = data.get('sex',('',''))[1]
    if '-' not in sex:
        result['sex_m' if sex == u'М' else 'sex_f' ] = 'X'

    passser, passno = split_num(get_val('passport_num'))
    result.update(gen_enum('passser',passser))
    result.update(gen_enum('passno',passno))

    update_date('passport_duration_from_date','passgot')
    update_date('passport_duration_till_date','passt')
    update_date('visa_delivery_date','visadel')
    update_date('visa_entrance_till_date','vst')
    update_date('migration_date','mgrd')
    update_date('migration_till_date','mgrt')
    update_enum('address_migration', 'mgra')

    visaser, visanum = split_num(get_val('visa_number'))
    result.update(gen_enum('visaser',visaser))
    result.update(gen_enum('visanum',visanum))

    mgrser, mgrnum = split_num(get_val('migration_number'))
    result.update(gen_enum('mgrs', mgrser))
    result.update(gen_enum('mgrn', mgrnum))


    #TODO add more
    return result