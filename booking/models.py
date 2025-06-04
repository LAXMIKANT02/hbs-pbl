from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
=======
from django.db.models.signals import post_save
from django.dispatch import receiver
>>>>>>> upstream

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    amenities = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, name=instance.username, email=instance.email, phone='')

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking by {self.customer.name} for {self.room} from {self.check_in} to {self.check_out}"

<<<<<<< HEAD
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True, null=True)
    min_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.location or 'Any Location'}"
=======
class HotelRating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='hotel_ratings')
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5

    class Meta:
        unique_together = ('hotel', 'customer')

    def __str__(self):
        return f"Rating {self.rating} by {self.customer.name} for {self.hotel.name}"
>>>>>>> upstream
