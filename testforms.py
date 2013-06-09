import re
from students.models import Student
from students.views import view_formats
def test_fields_existance():
    field_re = re.compile('form[.]([\w_]+)')
    fields = {f.name for f in Student._meta.fields if not f.name in f.name in ('id', 'studentrecordlock')}
    for file in view_formats:
        d = open('students/templates/'+file).read()
        found = field_re.findall(d)
        for f in found:
            if found.count(f) > 1:
                print "DOUBLING", f
        found_fields = set(found)
        print file, len(fields), len(found_fields)
        lost = fields - found_fields
        not_needed = found_fields - fields
        if lost: print "lost: ", list(lost)
        if not_needed: print "not needed:", found_fields - fields


test_fields_existance()
