from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Files)
admin.site.register(Victims)
admin.site.register(Food)
admin.site.register(Health)
admin.site.register(Shelter)
admin.site.register(Areas)
admin.site.register(UnstructuredTXT)
