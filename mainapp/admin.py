from django.contrib import admin
from .models import *

@admin.register(User)
class AdminUser(admin.ModelAdmin):
  list_display = ['first_name','last_name','username','email','is_mainadmin','is_tourist']

@admin.register(Mainadmin)
class MainadminUser(admin.ModelAdmin):
  list_display = ['user']

@admin.register(Tourist)
class TouristUser(admin.ModelAdmin):
  list_display = ['user','first_name','last_name','contact_no','age']

@admin.register(Categorys)
class Categorys(admin.ModelAdmin):
  list_display = ['c_name']

@admin.register(States)
class States(admin.ModelAdmin):
  list_display = ['s_name']


@admin.register(TourPlaces)
class TourPlaces(admin.ModelAdmin):
  list_display = ['state','description','placeImage','tour_active']
  

@admin.register(TourMorePlaces)
class TourMorePlace(admin.ModelAdmin):
  list_display = ['place_name','tourplace','description','show_categorys','placeImage']

  def show_categorys(self, ob):
        return ", ".join([category.c_name for category in ob.category.all()])

  
@admin.register(ReviewPack)
class AdminReviewAndRate(admin.ModelAdmin):
    list_display = ["r_user", "r_pack", "r_des", "rating"]