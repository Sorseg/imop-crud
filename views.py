#coding:utf8
from .forms import *
from .models import Student, StudentRecordLock, Country, user_permissions, Firm, \
    Institute
from datetime import datetime, date
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from pprint import pprint as pp
from time import time
import json
import time
import traceback
import os
import docs

view_formats = ['passport_form.html', 'omir_form.html', 'kadr_form.html']

def student_render(template=None, mimetype=None):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    and adds necessary items
    """

    def renderer(function):
        @login_required
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            new_view_format = request.GET.get('change_view')
            if request.GET.get('change_view') in view_formats:
                resp = HttpResponseRedirect(request.path)
                resp.set_cookie("view_format", new_view_format, max_age = 60*60*24*365)
                return resp
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            view_format = request.COOKIES.get('view_format', '')
            if not view_format in view_formats:
                view_format = view_formats[0]
            crit_cases = [{'count':func().count(), 'id':id, 'name':func.name} for id, func in Student.crit_cases.items()]
            output.update(
                          records_num = Student.objects.count(),
                          user_name = request.user.get_full_name(),
                          view_format = view_format,
                          crit_cases = crit_cases,
                          request = request)
            return render_to_response(tmpl, output, context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer


@student_render('search.html')
def search(request):
    perm = user_permissions(request.user,'R')
    if 'crit' in request.GET:
        search_class = request.GET['crit']
        search_name = '('+Student.crit_cases[search_class].name+')'
    else:
        search_name = ''
        search_class = ''

    return {'result_header': Student.get_table_header(perm),
            'search_name':search_name,
            'search_class':search_class}


@student_render('add.html')
def add(request):
    StudentForm = form_factory(request.user)
    if request.method != 'POST':
        return {'form': StudentForm()}
    else:
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                results = form.cleaned_data
                s = Student(**results)
                s.save()
            except Exception, e:
                return {'error':repr(e), 'form':form}
            else:
                #return {'success':s, 'form':StudentForm()}
                return HttpResponseRedirect(reverse('edit', args = (s.pk, )))
        return {'form':form}


@student_render('edit.html')
def edit(request, pk):

    #docs = [i for i in os.listdir(settings.DOCS_ROOT) if i.endswith('.rtf')]
    #docs = sorted(docs)
    result = {'pk': pk,
              #'docs': docs
              }
    s = get_object_or_404(Student, pk=pk)
    lock = s.studentrecordlock
    result['version'] = lock.version
    StudentForm = form_factory(request.user)
    if request.method == 'POST':
        if u'cancel' in request.POST:
            return HttpResponseRedirect(reverse('search'))
        if u'delete' in request.POST:
            s.delete()
            return HttpResponseRedirect(reverse('search'))
        if u'copy' in request.POST:
            s.pk = None
            s.save()
            return HttpResponseRedirect(reverse('edit', args = (s.pk, )))
        form = StudentForm(data = request.POST, instance = s)
        if request.POST.get('version','') == str(lock.version):
            if form.is_valid():
                with transaction.commit_on_success():
                    form.save()
                return HttpResponseRedirect(reverse('edit', args = (pk, )))
            else:
                result['form'] = form
                return result
        else:
            result['version_error'] = 'error'
            form = StudentForm(instance = s)
            result['form'] = forms
            return result
    else:
        form = StudentForm(instance = s)
        result['form'] = form
    return result


@student_render('docs.html')
def documents(request, pk):
    return {'pk':pk,
            'documents':[u'Уведомление.rtf']}


@student_render('view.html')
def view(request, pk):
    print "WARNING!!! View was called from", request.META.get('HTTP_REFERER','None')
    return HttpResponseRedirect(reverse('edit', args = (pk, )))


@student_render('card.html')
def test(request, pk):
    return {'params':request.GET, 'cookies':request.COOKIES, 'first_name':u"Test", 'last_name':u"Check"}


@login_required
@csrf_exempt
def ajax_search(request):
    perm = user_permissions(request.user,'R')
    parameters = request.POST
    response = {}
    response['sEcho'] = parameters.get('sEcho', '')
    #Filtering:
    search_conds = {}
    stud_fields = [f for f in Student.get_fields(perm).keys()]
    for i in range(1, int(parameters['iColumns'])):
        string=parameters['sSearch_'+str(i)]
        field_name = stud_fields[i-1]
        if not string:
            continue
        if field_name.endswith('date'):
            try:
                cond = datetime.strptime(string,'%d.%m.%Y')
            except:
                print "wrong date", repr(string)
                continue
            search_conds[field_name] = cond
        else:
            search_conds[field_name+'__icontains'] = string
    #Crit case filtering:
    if 'crit' in request.GET:
        seach_source = Student.crit_cases[request.GET['crit']]()
    else:
        seach_source = Student.objects

    search_result = seach_source.filter(**search_conds)

    #Sorting:
    order_fields = []
    sortcolnum = int(parameters['iSortingCols'])
    for i in range(sortcolnum):
        sortcol = parameters['iSortCol_'+str(i)]
        scindex = max(0, int(sortcol)-1)
        sc = stud_fields[scindex]
        if parameters['sSortDir_'+str(i)] == 'desc':
            sc = '-'+sc
        order_fields.append(sc)

    if order_fields:
        search_result = search_result.order_by(*order_fields)

    response['iTotalRecords'] = Student.objects.count()
    response['iTotalDisplayRecords'] = search_result.count()
    #TODO: response['sColumns'] = ['first_name','first_name_lat']
    aaData = []
    dispStart = int(parameters['iDisplayStart'])
    dispEnd = dispStart + int(parameters['iDisplayLength'])
    for record in search_result.all()[dispStart:dispEnd]:
        line = ['<a class="edit_link" href="{}">{}</a>'.format(reverse('edit', args = (record.pk, )), record.pk)]
        for name, value in record.get_dict(perm).values():
            line.append(value)
        aaData.append(line)
    response['aaData'] = aaData
    return HttpResponse(json.dumps(response), content_type="application/json")

@student_render('lists.html')
def lists(request):

    if request.method == 'POST':
        for Class, pref in [(Firm, 'firm'), (Institute, 'inst')]:
            if pref+'_add' in request.POST:
                name = request.POST.get(pref+'_add_name','')
                if name:
                    Class.objects.create(name=name)
            else:
                for key in request.POST.keys():
                    if key.startswith(pref+'_edit_'):
                        pk = int(key.split('_')[-1])
                        new_name = request.POST.get(pref+'_'+str(pk), '')
                        if new_name:
                            Class.objects.filter(pk=pk).update(name=new_name)
                    if key.startswith(pref+'_del_'):
                        pk = int(key.split('_')[-1])
                        Class.objects.get(pk=pk).delete()


    return {'firms':Firm.objects.all(),'institutes':Institute.objects.all()}


def countries(request):
    term = request.GET.get('term','')
    countries = []
    if term:
        countries = [c.name for c in Country.objects.filter(name__icontains = term)[:20]]
    print type(countries)
    return HttpResponse(json.dumps(countries), content_type='application/json')

@login_required
def doc_render(request, pk, doc):
    perm = user_permissions(request.user, 'R')
    s = get_object_or_404(Student, pk=pk)
    data = s.get_dict(perm)

    contents = docs.render(doc,data)
    doc_fname = os.path.basename(doc)
    #contents = open(os.path.join(settings.DOCS_ROOT, doc_fname)).read()

    response = HttpResponse(contents, content_type='application/rtf')
    response['Content-Disposition']='attachment; filename="'+doc_fname.encode('utf8')+'"'

    return response

