from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from .mail import booking_mail,Cancel_mail
from .models import *
from django.db.models import Q
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle , Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors 
from io import BytesIO
from rest_framework import generics
from .models import TourMorePlaces
from .serializers import PlacesSerializers




class PlacesView(generics.ListAPIView):
    queryset = TourMorePlaces.objects.all()
    serializer_class = PlacesSerializers



#______________________________________home___________________________________________

class Home(View):
    def get(self,request):
        qua =Quality.objects.all()
        tpm=TourPlaces.objects.all()
        k=CarouselM.objects.all()
        cat=Categorys.objects.all()
        all_pack = Packages.objects.all()
        places= TourMorePlaces.objects.all()



        return render(request,'home.html',{'k':k,'tpm':tpm,'cat':cat,'qua':qua,'pack':all_pack,'place':places})

#___________________________________about us_______________________________________
class Aboutus(View):
    def get(self,request):
        return render(request,'aboutus.html')

#___________________________________contact_______________________________________
class Contact(View):
    def get(self,request):
        return render(request,'contact.html')

#___________________________________updates_______________________________________
class Updates(View):
    def get(self,request):
        return render(request,'updates.html')


#___________________________________Document______________________________________
def Document(request):
    file_path = os.path.join('static', 'pdf', 'app_details.pdf')
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="app_details.pdf"'
        return response

#___________________________________updates_______________________________________
class Tandc(View):
    def get(self,request):
        return render(request,'t&c.html')


#___________________________________updates_______________________________________
class Privacy(View):
    def get(self,request):
        return render(request,'privacy.html')


#______________________________________search________________________________

class Search_view(View):
    def get(self,request):
        qua =Quality.objects.all()
        k=CarouselM.objects.all()
        cat=Categorys.objects.all()
        places= TourMorePlaces.objects.all()
        query = request.GET.get('q')

        if query:

            tpm = TourPlaces.objects.filter(
                Q(state__s_name__icontains=query) 
            )

            places = TourMorePlaces.objects.filter(
                Q(place_name__icontains=query) 
            )

            all_pack = Packages.objects.filter(
                Q(pack_name__icontains=query) 
            )
            if tpm.count() + places.count() + all_pack.count() == 0:
                messages.warning(self.request,f'there no place with name of {query}')


        else:
            tpm=''
            places=''
            all_pack=''
            messages.warning(self.request,f'there no place with name of {query}')


        return render(self.request,'home.html',{'k':k,'tpm':tpm,'cat':cat,'qua':qua,'pack':all_pack,'place':places})


# _______________________________________________________category___________________________________________________________

def category_view(request, id):
    qua =Quality.objects.all()
    k=CarouselM.objects.all()
    cat=Categorys.objects.all()
    all_pack = ""
    places= TourMorePlaces.objects.all()
    tpm=""

    try:
        category = Categorys.objects.get(pk=id)
        places = TourMorePlaces.objects.filter(category=category)
    except Categorys.DoesNotExist:
        places = ''
        messages.warning(request,f'Not available')

    return render(request,'home.html',{'k':k,'tpm':tpm,'cat':cat,'qua':qua,'pack':all_pack,'place':places})

    



#______________________________________tourist registration________________________________

class TouristRegister(CreateView):
    model = User
    form_class = TouristForm 
    k=True
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tourist'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


#________________________________________login for both user__________________________________
        
class LoginView(auth_views.LoginView):
    form_class = UserloginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_mainadmin:
                messages.success(self.request,'Succeessfully logged in')
                return reverse('mainadmin')
            else:
                messages.success(self.request,'Succeessfully logged in')
                return reverse('home')
        else:
            messages.warning(self.request,'spmething wrong')
            return reverse('Login')

#__________________________________________logout_________________________________________________

class UserLogout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'Logged Out Successfully')
        return redirect('home')


#____________________________________profile_________________________________

class Profile(View):
    def get(self, request):
        email = request.user
        tourist = Tourist.objects.get(user=request.user)
        data = {'contact_no': tourist.contact_no, 'age':tourist.age,'email': request.user.email}
        f=ProfileForm(initial=data)
        return render(request,'profileupdate.html',{'f':f,'t_user':tourist,'t_email':email})

    def post(self, request):
        tourist = Tourist.objects.get(user=request.user)
        form = ProfileForm(request.POST)

        if form.is_valid():
            tourist.contact_no = form.cleaned_data['contact_no']
            tourist.age = form.cleaned_data['age']
            tourist.save()
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()

            return redirect('profile')
        else:
            return render(request, 'profileupdate.html', {'f': form, 't_user': tourist, 't_email': request.user.email})








#_________________________________________Admin views___________________________________________________


class adRegister(CreateView):
    model = User
    form_class = adminForm
    template_name = 'adreg.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mainadmin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('mainadmin')




class MainAdmin(View):
    def get(self,request):
        st = States.objects.all()
        qu = Quality.objects.all() 
        tpm=TourPlaces.objects.all()
        return render(request,'mainadmin.html',{'tpm':tpm,'st':st,'qu':qu})
    



class Addtour(View):
    def get(self,request):
        f=tourPlaceForm
        return render(request,'addtour.html',{'f':f})
    
    def post(self,request):
        tour = tourPlaceForm(request.POST, request.FILES)
        
        if tour.is_valid():
            category = tour.cleaned_data.get('category')
            state = tour.cleaned_data.get('state')
            tours =tour.save(commit=False)
            tours.category =category
            tours.state =state
            tours.tour_active = True
            tours.save()
            messages.success(self.request,f'Added in tour')
            return redirect(to='mainadmin')

        else:
            messages.warning(self.request,f'Something went wrong ')
            return redirect(to='addtour')



class EditTourPlace(View):
    def get(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = tourPlaceForm(instance=m)
        return render(request, 'edittour.html', {'f': f, 'm': m})

    def post(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = tourPlaceForm(request.POST, request.FILES, instance=m)
        if f.is_valid():
            f.save()
            messages.success(request, 'Successfully Updated')
            return redirect('mainadmin')
        return render(request, 'edittour.html', {'f': f, 'm': m})




class DeleteTourPlace(View):
    def get(self, request, id):
        tour = get_object_or_404(TourPlaces, id=id)
        if tour:
            tour.delete()
            messages.success(request, 'Deleted Successfully')
        return redirect('mainadmin')


class AddState(View):
    def get(self, request):
        f = StateForm()
        return render(request, 'addstate.html', {'f': f})

    def post(self, request):
        f = StateForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "State Successfully Added")
            return redirect('mainadmin')
        else:
            messages.warning(request, "Something went wrong")
            return redirect('AddState')

class AddQuality(View):
    def get(self, request):
        f = QualityForm()
        return render(request, 'addquality.html', {'f': f})

    def post(self, request):
        f = QualityForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Quality Successfully Added")
            return redirect('mainadmin')
        else:
            messages.warning(request, "Something went wrong")
            return redirect('AddQuality')




#________________________________________Carousel views________________________________________
class CarouselView(View):
    def get(self, request):
        k = CarouselM.objects.all()
        f = CaroForm()
        ctp = CarouselM.objects.all()
        return render(request, 'carouselview.html', {'f': f, 'ctp': ctp, 'k': k})

    def post(self, request):
        f = CaroForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Successfully Updated')
            return redirect('carousel')
        return render(request, 'carouselview.html', {'f': f})
    

class CarouselEdit(View):
    def get(self, request, id):
        m = CarouselM.objects.get(id=id)
        f = CaroForm(instance=m)
        return render(request, 'editcarousel.html', {'f': f, 'm': m})

    def post(self, request, id):
        m = CarouselM.objects.get(id=id)
        f = CaroForm(request.POST, instance=m)
        if f.is_valid():
            f.save()
            messages.success(request, 'Successfully Updated')
            return redirect('carousel')
        else:
            messages.warning(request, 'Something went wrong')
            return render(request, 'editcarousel.html', {'f': f, 'm': m})


class DeleteCarousel(View):
    def get(self, request, id):
        caro = get_object_or_404(CarouselM, id=id)
        if caro:
            caro.delete()
            messages.success(request, 'Deleted Successfully')
        return redirect('carousel')




#________________________________________tour view____________________________________


class TourView(View):
    def get(self, request, id):
        m = TourPlaces.objects.get(id=id)
        all_p = TourMorePlaces.objects.filter(tourplace=id)
        all_pack = Packages.objects.filter(tourplace=id)
        return render(request, 'tourview.html', {'m': m, 'all_p': all_p, 'pack': all_pack})


#_______________________________________Manage place_________________________________


class ManagePlace(View):
    def get(self, request, id):
        m = TourPlaces.objects.get(id=id)
        all_p = TourMorePlaces.objects.filter(tourplace=id)
        all_pack = Packages.objects.filter(tourplace=id)
        return render(request, 'manageplace.html', {'m': m, 'all_p': all_p, 'pack': all_pack})

    def post(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = TourMorePlacesForm(request.POST, request.FILES)
        md = m.id
        tp = get_object_or_404(TourPlaces, pk=id)
        if f.is_valid():
            p_name = f.cleaned_data['place_name']
            desc = f.cleaned_data['description']
            p_image = f.cleaned_data['placeImage']
            s_link = f.cleaned_data['source_link']
            category = f.cleaned_data['category']
            mtp = TourMorePlaces.objects.create(
                tourplace=tp,
                place_name=p_name,
                description=desc,
                source_link=s_link,
                placeImage=p_image
            )
            mtp.category.set(category)
            mtp.save()
            messages.success(request, 'Successfully Added')
            return redirect('manageplace', id=md)
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('manageplace', id=md)







#_______________________________________Add place_________________________________


class AddPlace(View):
    def get(self, request, id):
        f = TourMorePlacesForm()
        return render(request, 'addplace.html', {'f': f})

    def post(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = TourMorePlacesForm(request.POST, request.FILES)
        md = m.id
        tp = get_object_or_404(TourPlaces, pk=id)
        if f.is_valid():
            p_name = f.cleaned_data['place_name']
            desc = f.cleaned_data['description']
            p_image = f.cleaned_data['placeImage']
            s_link = f.cleaned_data['source_link']
            category = f.cleaned_data['category']
            mtp = TourMorePlaces.objects.create(
                tourplace=tp,
                place_name=p_name,
                description=desc,
                source_link=s_link,
                placeImage=p_image
            )
            mtp.category.set(category)
            mtp.save()
            messages.success(request, 'Successfully Added')
            return redirect('manageplace', id=md)
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('addplace', id=md)




#_______________________________________Delete place_________________________________

class DeletePlace(View):
    def get(self, request, id):
        place = get_object_or_404(TourMorePlaces, id=id)
        tp_id = place.tourplace.id
        if place:
            place.delete()
            messages.success(request, 'Deleted Successfully')
        return redirect('manageplace', id=tp_id)



#_______________________________________add Package_________________________________


class AddPackage(View):
    def get(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = PackageForm()
        return render(request, 'addpackage.html', {'f': f})

    def post(self, request, id):
        m = TourPlaces.objects.get(id=id)
        f = PackageForm(request.POST)
        md = m.id
        tp = get_object_or_404(TourPlaces, pk=id)
        if f.is_valid():
            p_name = f.cleaned_data['pack_name']
            p_facility = f.cleaned_data['pack_facility']
            p_member = f.cleaned_data['pack_member']
            s_date = f.cleaned_data['start_date']
            e_date = f.cleaned_data['end_date']
            qua = f.cleaned_data['quality']
            p_price = f.cleaned_data['pack_price']
            mtp = Packages.objects.create(
                tourplace=tp,
                pack_name=p_name,
                pack_facility=p_facility,
                pack_member=p_member,
                quality=qua,
                start_date=s_date,
                end_date=e_date,
                pack_price=p_price
            )
            mtp.save()
            messages.success(request, 'Successfully Added')
            return redirect('manageplace', id=md)
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('addpackage', id=md)


 

#_______________________________________Delete package_________________________________

class DeletePackage(View):
    def get(self, request, id):
        pack = get_object_or_404(Packages, id=id)
        p_id = pack.tourplace.id
        if pack:
            pack.delete()
            messages.success(request, 'Deleted Successfully')
        return redirect('manageplace', id=p_id)
    


#_______________________________________Package view_________________________________

class PackageView(View):
    def get(self, request, id):
        pack = get_object_or_404(Packages, id=id)
        added_wish = WishList.objects.filter(
            w_pack=pack.id, user=request.user).first()
        tp_id = pack.tourplace.id
        tp = TourPlaces.objects.get(id=tp_id)
        mtp = TourMorePlaces.objects.filter(tourplace=tp_id)
        q_pack = Packages.objects.filter(tourplace=tp_id)
        rating = ReviewPack.objects.filter(r_pack=id)
        try:
            tourist = Tourist.objects.get(user=request.user)
            data = {'contact': tourist.contact_no, 'b_email': request.user.email}
            f = TourBookingForm(initial=data)
        except Tourist.DoesNotExist:
            f = TourBookingForm()
        r_form = ReviewForm()
        return render(request, 'packageview.html', {'f': f,'added_wish':added_wish,'r_form': r_form, 'rating': rating, 'pack': pack, 'tp': tp, 'mtp': mtp, 'q_pack': q_pack})



#_______________________________________book tour_________________________________

class BookTour(View):
    def get(self, request, id):
        return redirect('packageview', id=id)

    def post(self, request, id):
        form = TourBookingForm(request.POST)
        if form.is_valid():
            package = get_object_or_404(Packages, pk=id)
            booking = form.save(commit=False)
            if package.pack_member >= booking.b_members and booking.b_members >= 1 and booking.b_members <= 10:
                booking.b_pack = package
                booking.b_price = package.pack_price * booking.b_members 
                booking.b_user = request.user
                booking.save()
                tour = get_object_or_404(Packages, pk=id)
                tour.pack_member -= booking.b_members
                tour.save()
                messages.success(request, 'Booked Successfully, your booking details sent to your mail')
                bill = package.pack_price * booking.b_members
                pack_name = package.pack_name
                pack_start = package.start_date
                pack_end = package.end_date
                members = booking.b_members
                email = booking.b_email
                price = package.pack_price
                booking_mail(reciver_mail=email, bill=bill, pack_start=pack_start, pack_end=pack_end, package=pack_name, members=members, price=price)
            elif booking.b_members <= 0:
                messages.warning(request, 'Members cannot be zero or negative')
            elif booking.b_members >= 10:
                messages.warning(request, 'more then 10 members are not allowed')
            else:
                messages.warning(request, 'Not enough members available')
        else:
            messages.warning(request, 'Form is not valid')

        return redirect('packageview', id=id)






#_______________________________________Booking View_________________________________
class UserBooking(View):
    def get(self, request):
        bookings = Tourbooking.objects.filter(b_user=request.user)
        return render(request, 'showbooking.html', {'booked': bookings})





#______________________________________delete Bookings_________________________________
class CancelBookings(View):
    def get(self, request, id):
        booking = get_object_or_404(Tourbooking, id=id)

        if booking:
            package = booking.b_pack
            package.pack_member += booking.b_members
            package.save()

            booking.delete()
            messages.success(request, 'Cancelled Successfully')

            package = booking.b_pack
            bill = package.pack_price * booking.b_members
            pack_name = package.pack_name
            pack_start = package.start_date
            pack_end = package.end_date
            members = booking.b_members
            email = booking.b_email
            price = package.pack_price
            Cancel_mail(reciver_mail=email, bill=bill, pack_end=pack_end, pack_start=pack_start, package=pack_name, members=members, price=price)

        return redirect('showbookings')


#____________________________________review package___________________________________

class Reviews(View):
    def post(self, request, id):
        des = request.POST["r_des"]
        rating = request.POST["rating"]
        if rating:
            r_user = request.user
            r_pack = Packages.objects.get(id=id)
            f_r = ReviewPack(r_user=r_user, rating=rating, r_des=des, r_pack=r_pack)
            try:
                f_r.save()
                messages.success(request, "Review successfully added.")
            except ValidationError:
                messages.warning(request, "User can only leave one comment for a package.")
        else:
            messages.warning(request, "Please select a rating.")
        return redirect('packageview', id=id)
    



#____________________________________Wishlist___________________________________
class AddWishlist(View):
    def get(self, request, id):
        package_instance = Packages.objects.get(pk=id)
        data = WishList.objects.filter(
            w_pack=package_instance, user=request.user).first()
        if data is None:
            data = WishList(w_pack=package_instance, user=request.user)
            data.save()
            messages.success(
                request, f"{data.w_pack.pack_name} added to wishlist")
        else:
            data.delete()
            messages.success(
                request, f"{data.w_pack.pack_name} is deleted from wishlist")
        return redirect('packageview', id=id)



# ___________________________________adminBookingview_______________________________

class Allbookings(View):
    def get(self, request):
        bookings = Tourbooking.objects.all()
        return render(request,'adminbookings.html',{'bookings':bookings})
    


# ___________________________________wishlist view_______________________________

class Wishlistpage(View):
    def get(self, request):
        w_user = request.user
        pack = WishList.objects.filter(user=w_user)
        return render(request,'wishlist.html',{'pack':pack})
    


class Removewish(View):
    def get(self, request, id):
        data = WishList.objects.get(id=id,user=request.user )
        data.delete()
        messages.success(request, f"{data.w_pack.pack_name} is deleted from wishlist")
        return redirect('wishlist')


#________________________________________receipt___________________________________________

class receiptdownload(View):
    def get(self, request, id):
        user = request.user
        try:
            booking = Tourbooking.objects.get(id=id)
            package = Packages.objects.get(id=booking.b_pack.id)
            user_name = user.username
            user_email = user.email
            pack_name = package.pack_name
            pack_start = package.start_date
            pack_end = package.end_date
            members =  booking.b_members
            price = package.pack_price
            bill = members * price  

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()

            name_email = [
                Paragraph(f"Name: {user_name}", styles['Normal']),
                Paragraph(f"Email: {user_email}", styles['Normal']),
                Paragraph("<br/><br/>", styles['Normal']),
            ]

            elements.extend(name_email)


            receipt_details = [
                [f"Tour package","Date","Members","p/p price"],
                [ pack_name, f"{pack_start} to {pack_end}",str(members),f"{price} Rs"],
                ["","","Total bill:",f"{bill} Rs"]
            ]


            table = Table(receipt_details)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),  
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.antiquewhite),  
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  
            ]))

            elements.append(table)

            doc.build(elements)
            pdf = buffer.getvalue()
            buffer.close()

            response.write(pdf)
            return response

        except Packages.DoesNotExist:
            return HttpResponse("Package not found", status=404)









