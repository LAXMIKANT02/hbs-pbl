from django.core.management.base import BaseCommand
from booking.models import Hotel, Room, Customer, Booking
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Seed initial data for hotels, rooms, customers, and bookings'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Booking.objects.all().delete()
        Customer.objects.all().delete()
        Room.objects.all().delete()
        Hotel.objects.all().delete()

        media_path = os.path.join(os.getcwd(), 'media', 'hotel_images')

        # Create hotels
        hotel1 = Hotel(
            name='Grand Plaza',
            location='New York',
            rating=4.5,
            description='A luxurious hotel in the heart of New York.',
            amenities=['wifi', 'pool', 'gym']
        )
        image_path1 = os.path.join(media_path, 'grand_plaza.jpg')
        with open(image_path1, 'rb') as f:
            hotel1.image.save('grand_plaza.jpg', File(f), save=False)
        hotel1.save()

        hotel2 = Hotel(
            name='Sea View Resort',
            location='Miami',
            rating=4.0,
            description='Enjoy the beautiful sea view and sandy beaches.',
            amenities=['wifi', 'beach', 'spa']
        )
        image_path2 = os.path.join(media_path, 'sea_view_resort.jpg')
        with open(image_path2, 'rb') as f:
            hotel2.image.save('sea_view_resort.jpg', File(f), save=False)
        hotel2.save()

        # Create rooms for hotel1
        Room.objects.create(
            hotel=hotel1,
            room_type='Single',
            price=120.00,
            availability=True
        )
        Room.objects.create(
            hotel=hotel1,
            room_type='Double',
            price=180.00,
            availability=True
        )

        # Create rooms for hotel2
        Room.objects.create(
            hotel=hotel2,
            room_type='Suite',
            price=250.00,
            availability=True
        )
        Room.objects.create(
            hotel=hotel2,
            room_type='Double',
            price=200.00,
            availability=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded hotel, room, customer, and booking data with local images.'))
