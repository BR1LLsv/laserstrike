from django.shortcuts import render
from .models import Arena, Category
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Arena
from booking.forms import BookingForm
from booking.models import Booking
from datetime import datetime, timedelta, time
from decimal import Decimal


def index(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')

    arenas = Arena.objects.filter(is_available=True)

    # Фільтрація за категорією
    if selected_category:
        arenas = arenas.filter(category__slug=selected_category)

    # Пошук за назвою
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
            
            # 1. Валідація кількості гравців
            if booking.players_count > arena.max_players:
                form.add_error('players_count', f"Максимальна місткість цієї арени — {arena.max_players} осіб.")
            else:
                # 2. Розрахунок часу та вартості
                start_dt = datetime.combine(booking.booking_date, booking.start_time)
                end_dt = datetime.combine(booking.booking_date, booking.end_time)
                
                if end_dt <= start_dt:
                    form.add_error('end_time', "Час завершення має бути пізніше за час початку.")
                else:
                    # ---> ДОДАНО: Перевірка на перетин часу <---
                    overlapping_bookings = Booking.objects.filter(
                        arena=arena,
                        booking_date=booking.booking_date,
                        status__in=['new', 'paid'], # Ігноруємо скасовані (cancelled) та завершені
                        start_time__lt=booking.end_time,
                        end_time__gt=booking.start_time
                    )

                    if overlapping_bookings.exists():
                        # --- РОЗУМНИЙ ПОШУК ВІЛЬНОГО ЧАСУ ---
                        duration = end_dt - start_dt
                        
                        # Отримуємо всі активні бронювання на цю дату, відсортовані за часом
                        daily_bookings = Booking.objects.filter(
                            arena=arena,
                            booking_date=booking.booking_date,
                            status__in=['new', 'paid']
                        ).order_by('start_time')
                        
                        proposed_start = start_dt
                        
                        # Шукаємо найближче вільне "вікно" потрібної тривалості
                        for b in daily_bookings:
                            proposed_end = proposed_start + duration
                            b_start = datetime.combine(booking.booking_date, b.start_time)
                            b_end = datetime.combine(booking.booking_date, b.end_time)
                            
                            # Якщо пропонований час перетинається з цим бронюванням, 
                            # зсуваємо пропонований старт на момент завершення цього бронювання
                            if proposed_start < b_end and proposed_end > b_start:
                                proposed_start = b_end
                                
                        proposed_end = proposed_start + duration
                        
                        # Встановлюємо час закриття арени (наприклад, 22:00)
                        closing_time = datetime.combine(booking.booking_date, time(22, 0))
                        
                        # Якщо знайдений вільний час вміщується до закриття
                        if proposed_end <= closing_time:
                            suggested_time = f"{proposed_start.strftime('%H:%M')} - {proposed_end.strftime('%H:%M')}"
                            error_msg = f"Цей час вже зайнятий іншими гравцями. Найближче вільне вікно на таку ж тривалість: {suggested_time}."
                        else:
                            error_msg = "Цей час вже зайнятий, і на сьогодні більше немає вільних вікон такої тривалості. Будь ласка, оберіть іншу дату або зменште час гри."
                            
                        # Виводимо помилку у форму
                        form.add_error(None, error_msg)
                        # ------------------------------------
                    else:
                        # Якщо перетинів немає — зберігаємо як зазвичай
                        duration_hours = Decimal((end_dt - start_dt).total_seconds() / 3600)
                        booking.total_price = duration_hours * arena.price_per_hour
                        booking.status = 'new'
                        booking.save()
                        
                        messages.success(request, f"Бронювання №{booking.id} успішно створено!")
                        return redirect('pay_booking', booking_id=booking.id)
    else:
        form = BookingForm(initial={'players_count': 4})

    context = {
        'arena': arena,
        'form': form,
    }
    return render(request, 'catalog/arena_detail.html', context)

def shooting_range_view(request):
    """Страница интерактивного лазерного тира"""
    return render(request, 'catalog/shooting_range.html')