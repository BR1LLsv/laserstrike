import io
import base64
import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import PaymentForm


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'paid':
        messages.info(request, f"Бронювання №{booking.id} вже успішно оплачено.")
        return redirect('profile')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            booking.status = 'paid'
            booking.save()
            
            messages.success(request, f"Оплату успішно здійснено! Бронювання №{booking.id} підтверджено.")
            return redirect('profile')
    else:
        form = PaymentForm()

    return render(request, 'booking/payment.html', {'booking': booking, 'form': form})


@login_required
def ticket_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != 'paid':
        messages.error(request, "Квиток доступний лише після підтвердження оплати.")
        return redirect('profile')

    qr_data = (
        f"LASERSTRIKE TICKET #{booking.id}\n"
        f"User: {booking.user.username}\n"
        f"Arena: {booking.arena.title}\n"
        f"Date: {booking.booking_date}\n"
        f"Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}\n"
        f"Players: {booking.players_count}"
    )

    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'booking/ticket.html', {'booking': booking, 'qr_code': qr_base64})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        if booking.status == 'new':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, f"Бронювання №{booking.id} було успішно відмінено.")
        else:
            messages.error(request, "Це бронювання вже неможливо відмінити.")
            
    return redirect('profile')