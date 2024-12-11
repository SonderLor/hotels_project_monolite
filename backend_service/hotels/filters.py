from django.db.models import Q
from .models import Hotel
from rooms.models import Room

def search_accommodations(params):
    query = Q()

    if params.get("hotel"):
        query &= Q(name__icontains=params["hotel"])
    
    if params.get("hotel_type"):
        query &= Q(type__name__icontains=params["hotel_type"])
    
    if params.get("country"):
        query &= Q(country__icontains=params["country"])
    
    if params.get("city"):
        query &= Q(city__icontains=params["city"])
    
    hotels = Hotel.objects.filter(query).prefetch_related('rooms')

    query = Q()
    
    if params.get("room"):
        query &= Q(name__icontains=params["room"])

    if params.get("room_type"):
        query &= Q(type__name__icontains=params["room_type"])

    price_min = params.get("priceMin")
    price_max = params.get("priceMax")
    if price_min:
        query &= Q(price_per_night__gte=price_min)
    if price_max:
        query &= Q(price_per_night__lte=price_max)

    start_date = params.get("startDate")
    end_date = params.get("endDate")
    if start_date and end_date:
        query &= ~Q(
            Q(bookings__start_date__lt=end_date) &
            Q(bookings__end_date__gt=start_date)
        )

    hotel_ids = hotels.values_list('id', flat=True)
    rooms = Room.objects.filter(query, hotel_id__in=hotel_ids).select_related('hotel')

    sort_field = params.get("sort")
    if sort_field:
        rooms = rooms.order_by(sort_field)
    
    return hotels, rooms
