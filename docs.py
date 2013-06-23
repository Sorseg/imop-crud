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


CHESS_KEYS = ['fname_{:02}'.format(i) for i in range(1,36)]+\
             ['lname_{:02}'.format(i) for i in range(1,36)]+\
             ['cntry_{:02}'.format(i) for i in range(1,35)]+\
             gen_date_dict('bd').keys()+\
             ['sex_m','sex_f']+\
             ['passser_{:02}'.format(i) for i in range(1,5)]+\
             ['passno_{:02}'.format(i) for i in range(1,10)]+\
             gen_date_dict('passgot').keys()+\
             gen_date_dict('passt').keys()+\
             ['visaser_{:02}'.format(i) for i in range(1,5)]+\
             ['visanum_{:02}'.format(i) for i in range(1,10)]+\
             gen_date_dict('visadel').keys()+\
             gen_date_dict('vst').keys()+\
             gen_date_dict('mgrd').keys()+\
             gen_date_dict('mgrt').keys()+\
             ['mgrs_{:02}'.format(i) for i in range(1,5)]+\
             ['mgrn_{:02}'.format(i) for i in range(1,12)]+\
             ['mgra_{:02}'.format(i) for i in range(1,58)]

CHESS_PATTERN = re.compile('(' + '|'.join(CHESS_KEYS) + r')')


def test():
    with open('docs/design_filling4.rtf') as f:
        data = f.read()

    pattern = re.compile('(' + '|'.join(CHESS_KEYS) + r')')
    result = pattern.sub(lambda x:random.choice(string.letters),data)


    with open('asdf.rtf','w') as fo:
        fo.write(result.encode('cp1251'))

def render(doc, data):
    doc_fname = os.path.basename(doc)
    contents = open(os.path.join(settings.DOCS_ROOT, doc_fname.encode('utf8'))).read()
    if doc == u'Уведомление.rtf':
        uv_replace = gen_chess_data(data)
        result = CHESS_PATTERN.sub(lambda x:uv_replace.get(x.group(),''), contents)
        return result

def gen_chess_data(data):
    result = {}
    def update_enum(key, pref):
        val = data.get(key,('',''))[1].upper()
        if val not in ('','-'):
            result.update(gen_enum(pref,val))

    def update_date(key,pref):
        val = data.get(key,('',''))[1]
        if val not in ('','-'):
            result.update(gen_date_dict(pref,val))
    #WARNING!!!! fname and lname are swapped in file
    update_enum('first_name','lname')
    update_enum('last_name','fname')
    update_enum('citizenship','cntry')
    update_date('birth_date','bd')

    #TODO add more
    return result