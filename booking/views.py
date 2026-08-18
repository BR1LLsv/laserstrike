from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import PaymentForm
import io
import base64
import qrcode


@login_required
def payment_view(request, booking_id):
    # Отримуємо бронювання ТІЛЬКИ поточного користувача (захист від IDOR)
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Якщо бронювання вже оплачене — перенаправляємо в кабінет
    if booking.status == 'paid':
        messages.info(request, f"Бронювання №{booking.id} вже успішно оплачено.")
        return redirect('profile')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Імітація успішного транзакційного еквайрингу
            booking.status = 'paid'
            booking.save()
            
            messages.success(request, f"Оплату успішно здійснено! Бронювання №{booking.id} підтверджено.")
            return redirect('profile')
    else:
        form = PaymentForm()

    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'booking/payment.html', context)

@login_required
def ticket_view(request, booking_id):
    # Отримуємо бронювання лише поточного користувача
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Доступ до квитка є тільки у підтверджених (оплачених) бронювань
    if booking.status != 'paid':
        messages.error(request, "Квиток доступний лише після підтвердження оплати.")
        return redirect('profile')

    # Формуємо дані для зчитування сканером на арені
    qr_data = (
        f"LASERSTRIKE TICKET #{booking.id}\n"
        f"User: {booking.user.username}\n"
        f"Arena: {booking.arena.title}\n"
        f"Date: {booking.booking_date}\n"
        f"Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}\n"
        f"Players: {booking.players_count}"
    )

    # Генерація QR-коду в пам'яті
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")

    # Конвертація зображення в Base64 для вставки прямо в HTML
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'booking': booking,
        'qr_code': qr_base64,
    }
    return render(request, 'booking/ticket.html', context)

@login_required
def cancel_booking(request, booking_id):
    # Отримуємо бронювання лише поточного користувача для безпеки
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Перевіряємо, чи можна його скасувати
        if booking.status == 'new':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, f"Бронювання №{booking.id} було успішно відмінено.")
        else:
            messages.error(request, "Це бронювання вже неможливо відмінити.")
            
    return redirect('profile')