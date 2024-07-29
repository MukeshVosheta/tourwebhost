"""
URL configuration for tour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .decorators import mainadmin_required

urlpatterns = [
    # ___________________________________Home access________________________________________


     path('places/',views.PlacesView.as_view(), name='places'),
    path('',views.Home.as_view(),name='home'),
    path('Sign-up',views.TouristRegister.as_view(),name='register'),
    path('adreg',views.adRegister.as_view(),name='adregis'),
    path('Sign-in',views.LoginView.as_view(),name='Login'),
    path('logout',views.UserLogout.as_view(),name='logout'),
    path('Tour-View/<int:id>/',views.TourView.as_view(),name='tourview'),
    path('search/', views.Search_view.as_view(), name='search'),
    path('category/<int:id>/', views.category_view, name='category'),
    path('aboutus/', views.Aboutus.as_view(), name='aboutus'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('updates/', views.Updates.as_view(), name='updates'),
    path('document/', views.Document, name='document'),
    path('t&c/', views.Tandc.as_view(), name='t&c'),
    path('Privacy/', views.Privacy.as_view(), name='privacy'),


    



    # _______________________________Admin access_____________________________________________

    path('AdminSite',login_required(mainadmin_required(views.MainAdmin.as_view())) ,name='mainadmin'),
    path('Add-tour',login_required(mainadmin_required(views.Addtour.as_view())) ,name='addtour'),
    path('EditTour/<int:id>/',login_required(mainadmin_required(views.EditTourPlace.as_view())) ,name='EditTour'),
    path('DeleteTour/<int:id>/',login_required(mainadmin_required(views.DeleteTourPlace.as_view())) ,name='DeleteTour'),
    path('Carousel-View',login_required(mainadmin_required(views.CarouselView.as_view())) ,name='carousel'),
    path('Carousel-Edit/<int:id>/',login_required(mainadmin_required(views.CarouselEdit.as_view())) ,name='carouseledit'),
    path('Carousel-delete/<int:id>/',login_required(mainadmin_required(views.DeleteCarousel.as_view())) ,name='Deletecarousel'),
    path('Add-State/',login_required(mainadmin_required(views.AddState.as_view())),name='AddState'),
    path('Add-Quality/',login_required(mainadmin_required(views.AddQuality.as_view())),name='AddQuality'),
    path('Manage-Place/<int:id>/',login_required(mainadmin_required(views.ManagePlace.as_view())),name='manageplace'),
    path('Add-Place/<int:id>/',login_required(mainadmin_required(views.AddPlace.as_view())),name='addplace'),
    path('Add-Package/<int:id>/',login_required(mainadmin_required(views.AddPackage.as_view())),name='addpackage'),
    path('Delete-Package/<int:id>/',login_required(mainadmin_required(views.DeletePackage.as_view())),name='deletepack'),
    path('Delete-Place/<int:id>/',login_required(mainadmin_required(views.DeletePlace.as_view())),name='DeletePlace'),
    path('All-bookings/',login_required(mainadmin_required(views.Allbookings.as_view())),name='allbookings'),
    
    




    #________________________________User access___________________________________________
    
    path('package/<int:id>/',login_required(views.PackageView.as_view()),name='packageview'),
    path('Book-Tour/<int:id>/',login_required(views.BookTour.as_view()),name='booktour'),
    path('Show-bookings/',login_required(views.UserBooking.as_view()),name='showbookings'),
    path('Delete-booking/<int:id>/',login_required(views.CancelBookings.as_view()),name='cancelbooking'),
    path('Review-package/<int:id>/',login_required(views.Reviews.as_view()) ,name='addreview'),
    path('add-wishlist/<int:id>/',login_required(views.AddWishlist.as_view()) ,name='addwishlist'),
    path('wishlist',login_required(views.Wishlistpage.as_view()) ,name='wishlist'),
    path('removewish/<int:id>/',login_required(views.Removewish.as_view()) ,name='removewish'),
    path('profile/',login_required(views.Profile.as_view()) ,name='profile'),
    path('receipt/<int:id>/',login_required(views.receiptdownload.as_view()) ,name='receipt'),








 

    
]




