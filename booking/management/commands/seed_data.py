import csv
from django.core.management.base import BaseCommand
from booking.models import Hotel, Room, Customer, Booking
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed initial data for Indian hotels, rooms, customers, and bookings using CSV and local images'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Booking.objects.all().delete()
        Customer.objects.all().delete()
        Room.objects.all().delete()
        Hotel.objects.all().delete()

        # Path to CSV file
        csv_path = os.path.join(settings.BASE_DIR, 'hotels_india.csv')
        # Local images directory path
        images_dir = os.path.join(settings.BASE_DIR, 'media', 'hotel_images')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        if not os.path.exists(images_dir):
            self.stdout.write(self.style.ERROR(f'Images directory not found at {images_dir}'))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                if count >= 60:
                    break
                name = row['name']
                location = row['location']
                description = row['description']
                price_per_night = float(row['price_per_night']) if row['price_per_night'] else 100.0
                image_filename = row['image']

                hotel = Hotel(
                    name=name,
                    location=location,
                    description=description,
                    rating=4.0,  # default rating
                    amenities=[]  # empty amenities, can be updated later
                )

                image_path = os.path.join(images_dir, image_filename)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        hotel.image.save(image_filename, File(img_file), save=False)
                else:
                    self.stdout.write(self.style.WARNING(f'Image file {image_filename} not found for hotel {name}'))

                hotel.save()

                # Create 2 rooms per hotel with price from CSV for standard and deluxe
                Room.objects.create(
                    hotel=hotel,
                    room_type='Standard',
                    price=price_per_night,
                    availability=True
                )
                Room.objects.create(
                    hotel=hotel,
                    room_type='Deluxe',
                    price=price_per_night * 1.5,
                    availability=True
                )
                count += 1

        self.stdout.write(self.style.SUCCESS('Successfully seeded 60 Indian hotels with CSV data and local images.'))
