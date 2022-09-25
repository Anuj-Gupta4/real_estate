from django.contrib import admin

# Register your models here.
from .models import Listing

admin.site.register(Listing)

# class ListingAdmin(admin.ModelAdmin):
#     def save_model(self, request, instance, form, change):
#         user = request.user 
#         instance = form.save(commit=False)
#         if not change or not instance.owner:
#             instance.owner = user
#         instance.save()
#         form.save_m2m()
#         return instance