from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError




#_____________________________Create diffrent users___________________________

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_mainadmin = models.BooleanField(default=False)
    is_tourist= models.BooleanField(default=False)




#_____________________________Main admin___________________________

class Mainadmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Mainadmin')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)





#_____________________________Tourist___________________________

class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Tourist')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=10)
    age = models.CharField(max_length=10)





#_____________________________Category___________________________

class Categorys(models.Model):
    c_name = models.CharField(max_length=50)
    def __str__(self):
        return self.c_name





#_____________________________state___________________________

class States(models.Model):
    s_name = models.CharField(max_length=50)
    def __str__(self):
        return self.s_name






#_____________________________quality___________________________

class Quality(models.Model):
    q_name = models.CharField(max_length=50)
    def __str__(self):
        return self.q_name







#_____________________________TourPlace___________________________

class TourPlaces(models.Model):
    state = models.ForeignKey(States, on_delete=models.SET_NULL,null=True)
    description = models.CharField(max_length=1000, null=False, blank=False)
    placeImage = models.ImageField(null=False, blank=False, upload_to='places/')
    tour_active = models.BooleanField(default=False)

    def __str__(self):
        return self.state.s_name




 


#____________________________Tourmoreplaces________________________________

class TourMorePlaces(models.Model):
    tourplace=models.ForeignKey(TourPlaces, on_delete=models.SET_NULL,null=True)
    place_name=models.CharField(max_length=200,null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)
    category = models.ManyToManyField(Categorys)
    source_link = models.URLField(max_length=1000)
    placeImage = models.ImageField(null=False, blank=False, upload_to='moreplaces/')




#_____________________________Package___________________________

class Packages(models.Model):
    
    tourplace= models.ForeignKey(TourPlaces, on_delete=models.CASCADE)
    pack_name = models.CharField(max_length=200, null=False, blank=False)
    pack_facility = models.CharField(max_length=1000, null=False, blank=False)
    pack_member = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    quality = models.ForeignKey(Quality, on_delete=models.SET_NULL,null=True)
    pack_price = models.IntegerField()


#_____________________________CarosualAds___________________________

class CarouselM(models.Model):
    t_place = models.ForeignKey(TourPlaces,on_delete=models.CASCADE,null=True)



    
#_____________________________tourbooking____________________________

class Tourbooking(models.Model):
    b_user = models.ForeignKey(User, on_delete=models.CASCADE)
    b_pack = models.ForeignKey(Packages, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    b_email = models.EmailField()
    b_members = models.SmallIntegerField()
    b_price = models.IntegerField()



#______________________________reviws________________________________

class ReviewPack(models.Model):
    rating_choose = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    r_pack = models.ForeignKey(Packages, on_delete=models.CASCADE)
    r_user = models.ForeignKey(User, on_delete=models.CASCADE)
    r_des = models.CharField(max_length=1000, default=None)
    r_upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=rating_choose, default=1)

    class Meta:
        unique_together = ('r_pack', 'r_user',)

    def __str__(self):
        return f"{self.id}"

    def return_list(self):
        return [i for i in range(self.rating)]

    def length(self):
        return [i for i in range(5)]
    
    def save(self, *args, **kwargs):
        existing_review = ReviewPack.objects.filter(r_pack=self.r_pack, r_user=self.r_user)
        if existing_review.exists() and not self.pk:
            raise ValidationError("")
        super(ReviewPack, self).save(*args, **kwargs)




# _______________________________________Wishlist__________________________________________

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    w_pack = models.ForeignKey(Packages, on_delete=models.CASCADE)







