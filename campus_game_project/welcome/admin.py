from django.contrib import admin
from welcome.models import User, Admin

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
