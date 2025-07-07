from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Tour
from .models import CustomUser
from .forms import *
from .forms import EmailLoginForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour
from .forms import TourForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
# Register view
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Tour
import io

from datetime import datetime
from .models import MonthlyPick
# views.py
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def generate_otp():
    return str(random.randint(100000, 999999))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            otp = generate_otp()
            user.email_otp = otp
            user.save()

            request.session['user_id'] = user.id


            current_site = get_current_site(request)
            subject = '✉️ Verify your email with Travel Explorer OTP'
            html_message = render_to_string('registration/verify_email.html', {
                'user': user,
                'otp': otp,
                'domain': current_site.domain,
            })
            # send_mail(subject, message, 'admin@site.com', [user.email])
            # send_mail(subject, html_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email = EmailMessage(
                subject,
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.content_subtype = 'html'  # Important for rendering HTML
            email.send()
            

            return redirect('verify_email')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def verify_email(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == user.email_otp:
            user.is_active = True
            user.is_verified = True
            user.email_otp = ''
            user.save()
            messages.success(request, 'Email verified successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'registration/verify_otp.html', {'email': user.email})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = generate_otp()
            user.email_otp = otp
            user.save()
            request.session['reset_user_id'] = user.id
            send_mail("Password Reset OTP", f"Your OTP is: {otp}", "admin@site.com", [email])
            return redirect('verify_reset_otp')
        else:
            messages.error(request, "No user found with this email.")
    return render(request, 'registration/forgot_password.html')



def verify_reset_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == user.email_otp:
            return redirect('reset_password')
        messages.error(request, "Invalid OTP.")
    return render(request, 'registration/verify_reset_otp.html')



def reset_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.email_otp = ''
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'registration/reset_password.html')




# Email verification link view
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        return redirect('/login/')
    return render(request, 'registration/invalid_link.html')


def email_login_view(request):
    form = EmailLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data.get('user')
        login(request, user)
        return redirect('home')  # or your dashboard
    return render(request, 'registration/login.html', {'form': form})

class LogoutViewAllowGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
# def home_view(request):
#     tours = Tour.objects.filter(is_active=True)

#     query = request.GET.get('q')
#     if query:
#         tours = tours.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))

#     # Additional filters
#     if 'price' in request.GET:
#         sort = request.GET.get('price')
#         if sort == 'low':
#             tours = tours.order_by('price')
#         elif sort == 'high':
#             tours = tours.order_by('-price')

#     paginator = Paginator(tours, 10)
#     page = request.GET.get('page')
#     tours = paginator.get_page(page)

#     return render(request, 'tours/home.html', {'tours': tours})
def home_view(request):
    tours = Tour.objects.filter(is_active=True)
    query = request.GET.get('q')
    destination = request.GET.get('destination')
    food = request.GET.get('food_type')
    tour_type = request.GET.get('tour_type')
    duration = request.GET.get('duration')
    available_from = request.GET.get('available_from')
    price_sort = request.GET.get('price')

    current_month = str(datetime.now().month)
    top_picks = MonthlyPick.objects.filter(month=current_month)

    if query:
        tours = tours.filter(Q(name__icontains=query))

    if destination:
        tours = tours.filter(Q(city__icontains=destination) | Q(country__icontains=destination))

    if food:
        tours = tours.filter(food_type__iexact=food)

    if tour_type:
        tours = tours.filter(tour_type__iexact=tour_type)

    if duration:
        if duration == "1-3":
            tours = tours.filter(duration_days__gte=1, duration_days__lte=3)
        elif duration == "4-7":
            tours = tours.filter(duration_days__gte=4, duration_days__lte=7)
        elif duration == "8":
            tours = tours.filter(duration_days__gt=7)

    if available_from:
        tours = tours.filter(availability_date__gte=available_from)

    if price_sort == "low":
        tours = tours.order_by("price")
    elif price_sort == "high":
        tours = tours.order_by("-price")

    paginator = Paginator(tours, 10)
    page = request.GET.get('page')
    tours = paginator.get_page(page)

    return render(request, 'tours/home.html', {'tours': tours,'top_picks': top_picks,})

# Add tour
@login_required
def add_tour(request):
    if request.method == 'POST':
        form = TourForms(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.user = request.user
            tour.save()
            return redirect('/')
    else:
        form = TourForms()
    return render(request, 'tours/add_tour.html', {'form': form})

# Tour Detail View

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'tours/tour_detail.html', {'tour': tour})


def custom_logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def user_dashboard(request):
    query = request.GET.get('q')
    tours = Tour.objects.filter(user=request.user)

    if query:
        tours = tours.filter(name__icontains=query)

    paginator = Paginator(tours.order_by('-created_at'), 10)
    page = request.GET.get('page')
    page_tours = paginator.get_page(page)

    return render(request, 'tours/dashboard.html', {
        'tours': page_tours,
        'query': query,
    })




def tour_pdf_view(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    template_path = 'tours/tour_pdf.html'
    context = {'tour': tour}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="tour_{tour.id}.pdf"'

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode('utf-8')), dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had errors while generating PDF')
    return response



@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, user=request.user)

    if request.method == 'POST':
        form = ToursForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ToursForm(instance=tour)

    return render(request, 'tours/edit_tour.html', {'form': form, 'tour': tour})
