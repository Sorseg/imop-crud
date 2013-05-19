#encoding:utf8
from django.forms import ModelForm, HiddenInput
from .models import Student, user_permissions


class ReadOnlyField:
    
    def __init__(self, name, value):
        self.label = name
    
    def __unicode__(self):
        return self.value


def form_factory(user):
    
    w_perm = user_permissions(user, 'W')
    r_perm = user_permissions(user, 'R')
    
    class StudentForm(ModelForm):
        
        @property
        def vis_fields(self):
            fields = self.visible_fields()
            for f in fields:
                if hasattr(f.field, 'choices') and f.value():
                    f.visible_value = dict(f.field.choices)[f.value()]
                else:
                    f.visible_value = f.value()
            return fields
        
        
        def disable(self):
            for v in self.fields.values():
                v.widget.attrs['disabled'] = True
                
        def _post_clean(self):
            for d in self.fields.keys():
                if d not in w_perm and d in self.cleaned_data:
                    del self.cleaned_data[d]  
            super(StudentForm, self)._post_clean()          
                
                
        def __init__(self, *a, **kw):
            super(StudentForm, self).__init__(*a,**kw)     
            for id, f in self.fields.items():
                if id not in w_perm:
                    f.widget.attrs['disabled'] = True
                if id.endswith('date'):
                    f.input_formats = ['%d.%m.%Y']
                f.required = False

        class Meta:
            model = Student
            fields = w_perm | r_perm
        
                
    return StudentForm
