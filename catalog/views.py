from datetime import datetime, time
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Arena, Category
from booking.forms import BookingForm
from booking.models import Booking


def index(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')

    arenas = Arena.objects.filter(is_available=True)

    if selected_category:
        arenas = arenas.filter(category__slug=selected_category)

    if search_query:
        arenas = arenas.filter(title__icontains=search_query)

    context = {
        'categories': categories,
        'arenas': arenas,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'catalog/index.html', context)


def arena_detail(request, pk):
    arena = get_object_or_404(Arena, pk=pk, is_available=True)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Для бронювання арени необхідно увійти до акаунту.")
            return redirect('login')
            
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.arena = arena
            
            if booking.players_count > arena.max_players:
                form.add_error('players_count', f"Максимальна місткість цієї арени — {arena.max_players} осіб.")
            else:
                start_dt = datetime.combine(booking.booking_date, booking.start_time)
                end_dt = datetime.combine(booking.booking_date, booking.end_time)
                
                if end_dt <= start_dt:
                    form.add_error('end_time', "Час завершення має бути пізніше за час початку.")
                else:
                    overlapping_bookings = Booking.objects.filter(
                        arena=arena,
                        booking_date=booking.booking_date,
                        status__in=['new', 'paid'],
                        start_time__lt=booking.end_time,
                        end_time__gt=booking.start_time
                    )

                    if overlapping_bookings.exists():
                        duration = end_dt - start_dt
                        daily_bookings = Booking.objects.filter(
                            arena=arena,
                            booking_date=booking.booking_date,
                            status__in=['new', 'paid']
                        ).order_by('start_time')
                        
                        proposed_start = start_dt
                        
                        for b in daily_bookings:
                            proposed_end = proposed_start + duration
                            b_start = datetime.combine(booking.booking_date, b.start_time)
                            b_end = datetime.combine(booking.booking_date, b.end_time)
                            
                            if proposed_start < b_end and proposed_end > b_start:
                                proposed_start = b_end
                                
                        proposed_end = proposed_start + duration
                        closing_time = datetime.combine(booking.booking_date, time(22, 0))
                        
                        if proposed_end <= closing_time:
                            suggested_time = f"{proposed_start.strftime('%H:%M')} - {proposed_end.strftime('%H:%M')}"
                            error_msg = f"Цей час вже зайнятий іншими гравцями. Найближче вільне вікно на таку ж тривалість: {suggested_time}."
                        else:
                            error_msg = "Цей час вже зайнятий, і на сьогодні більше немає вільних вікон такої тривалості. Будь ласка, оберіть іншу дату або зменште час гри."
                            
                        form.add_error(None, error_msg)
                    else:
                        duration_hours = Decimal((end_dt - start_dt).total_seconds() / 3600)
                        booking.total_price = duration_hours * arena.price_per_hour
                        booking.status = 'new'
                        booking.save()
                        
                        messages.success(request, f"Бронювання №{booking.id} успішно створено!")
                        return redirect('pay_booking', booking_id=booking.id)
    else:
        form = BookingForm(initial={'players_count': 4})

    return render(request, 'catalog/arena_detail.html', {'arena': arena, 'form': form})


def shooting_range_view(request):
    return render(request, 'catalog/shooting_range.html')