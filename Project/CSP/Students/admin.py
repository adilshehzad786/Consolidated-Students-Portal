from django.contrib import admin
from Students.models import Student, SGPA, Record, Marks,marksupload





admin.site.register(marksupload)
admin.site.register(Student)
admin.site.register(SGPA)
admin.site.register(Record)
admin.site.register(Marks)



