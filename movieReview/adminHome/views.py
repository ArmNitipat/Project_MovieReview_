from django.db import transaction
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create your views here.
# from .forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import login, authenticate, logout

from star.models import *
from movies.models import *
from .forms import CommentForm, SignupForm
from datetime import date
from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from .forms import SignupForm

from .models import *

#---------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from adminHome.models import Premium, Premium_list
#---------------------------------------------

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Here, you can save any additional data or perform other operations as required
#             return redirect('login')  # or redirect to some other page
#     else:
#         form = SignupForm()
#     return render(request, 'your_template_name.html', {'form': form})

# from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
# Calendar scraper
def calendarscraper(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = 'https://www.boxofficemojo.com/calendar/'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    name_list = []
    tag_list = []
    actor_list = []
    image_list = []

    for m in soup.find_all('td', {'class': 'a-text-left mojo-header-column mojo-truncate mojo-field-type-release mojo-cell-wide'}):
        moviename = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-release-details'})
        movietag = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-genres'})

        if moviename:
            name_list.append(moviename.find('a').text)
        else:
            name_list.append("Don't have name")

        if movietag:
            tag_list.append(movietag.text.replace('\n','').replace('            ',' ').replace('    ',''))
        else:
            tag_list.append("No Tag")

        with_divs = m.find_all('div', {'class': 'a-section a-spacing-none'})
        filtered_with_divs = [div for div in with_divs if div.find('span', {'class': 'a-text-bold'})]

        if filtered_with_divs:
            actor_list.append(filtered_with_divs[0].text.replace('With:',''))
        else:
            actor_list.append("No Actor")

        img_tag = m.find('img')
        if img_tag:
            image_list.append(img_tag.get('src'))
        else:
            image_list.append("No Image")

    context = {
        'name_list': name_list,
        'tag_list': tag_list,
        'actor_list': actor_list,
        'image_list': image_list,
    }

    return render(request, 'calender.html', context)

def test(request):
    template = loader.get_template('Loy Krathong Day.html')
    return HttpResponse(template.render())

# 404 page
def handler404(request, *args, **argv):
    response = render('404.html', {},
    context_instance=RequestContext(request))
    response.status_code = 404
    return response

# search.html 
def search(request):
    search_query = request.GET.get('q', '')  # รับค่าจากคิวรีพารามิเตอร์ 'q'
    # search_query = search.replace(" ", "") # ฟังก์ชั่นฟวย
    stars = []  # เริ่มต้นด้วยลิสต์ว่างสำหรับ stars
    movies =[]
    stars_images = [] # เริ่มต้นด้วยลิสต์ว่างสำหรับ star image 
    movies_images = []
    context = {}
    try:
        search_year = int(search_query)
        year_lookup = True
    except ValueError:
        year_lookup = False
    if search_query:  # ถ้ามีการค้นหาที่ส่งมา

        if year_lookup:
            stars = Star.objects.filter(born_date__year=search_year)
        else:
            stars = Star.objects.filter(name__icontains=search_query)  # ค้นหาดาราที่มีชื่อตรงกับคำค้น !!(name_icontains = search ) ==== (sql) WHERE headline ILIKE '%ชื่อ%'; 
        
        for star in stars:
            # Get the main image for each star
            main_image = star.local_star_images.filter(mainstar=True, is_visible=True).first()
            if not main_image:
                main_image = star.url_star_images.filter(mainstar=True, is_visible=True).first()
            
            stars_images.append({
                'star': star,
                'main_image': main_image,
            })

        if year_lookup:
            movies = Movie.objects.filter(release_date__year=search_year)
        else:
            # หาก search_query ไม่ใช่ปี ให้ค้นหาตามชื่อ
            movies = Movie.objects.filter(name__icontains=search_query)
        
        for movie in movies:
            # ภาพหลักหรับหนังแต่ละเรื่อง
            main_local_image = movie.local_images_movie.filter(mainmovie=True, is_visible=True).first()
            
            # ภาพ URL หลักหรับหนังแต่ละเรื่อง
            main_url_image = movie.url_movie_images.filter(mainmovie=True, is_visible=True).first()

            # Determine which main image to use
            main_image = main_local_image or main_url_image

            movies_images.append({
                'movie': movie,
                'main_image': main_image,
            })

        print(stars)
        context={
            'search_query':search_query,
            'star':stars,
            'stars_images': stars_images,
            'movie':movies,
            'movies_images':movies_images,

        }# context จะถูกส่งไปยัง template ทุกครั้ง แต่จะมี stars เฉพาะเมื่อมีการค้นหา
    return render(request, 'search.html', context)


@login_required
def update_user(request):
    if request.method == 'POST':
        # รับข้อมูลจาก POST request
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname')
        new_email = request.POST.get('email')
        new_image = request.FILES.get('profile_image')
        user = request.user

        # อัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
        if new_email != user.email and User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
            messages.error(request, 'There is already a user using this email.')
            return redirect('settingprofile')
        
        user = request.user
        user.first_name = new_firstname
        user.last_name = new_lastname
        user.email = new_email
        user.save()
        
        # ถ้ามีรูปภาพเก่าในโมเดล, ลบมัน
        if new_image:
            if user.image and user.image.name != 'profile_images/istockphoto612x612.jpg':
                user.image.delete(save=False)
            user.image = new_image
            user.save()
        messages.success(request, 'ข้อมูลของคุณถูกอัปเดตแล้ว')
        return redirect('settingprofile')  # ลิงก์ไปยังหน้าโปรไฟล์หลังจากอัปเดตข้อมูล
    return redirect('account')


@login_required
def get_user_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


def signup_view(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # email = request.POST.get('email')
        form = SignupForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(commit=False)
            send_mail(
                'Movie Review การสมัครสมาชิก',
                f'เรายินดีที่ คุณ {user.username} ได้มาเป็นสมาชิกกับเรา',
                'your-email@gmail.com',
                [user.email],  # Add recipient list here
                fail_silently=False,
            )
            if not user.image:
                user.image = 'profile_images/istockphoto612x612.jpg' 
                user.save()
            login(request, user)
            return redirect('home')  # Redirect to a 'home' view, for instance.
    else:
        form = SignupForm()
    return render(request, 'Login_Register/register.html', {'form': form}) #form จะถูกหรือไม่ view จะส่งกลับ HttpResponse ในทุกสถานการณ์.

#Login
def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            context['login_error'] = "This username and password could not be found."
    return render(request, 'Login_Register/login.html', context)


def resetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # ตรวจสอบว่ามีผู้ใช้ที่ตรงกับ username และ email ในฐานข้อมูลหรือไม่
        user = User.objects.filter(username=username, email=email).exists()
        if user:
            # ถ้าผ่านการตรวจสอบ, ไปที่หน้า resetpassword2
            return redirect(user,'resetpassword2')
        else:
            messages.error(request, 'ไม่พบผู้ใช้ที่มีชื่อผู้ใช้และอีเมลนี้')
            return render(request, 'Login_Register/resetpassword.html')

    return render(request, 'Login_Register/resetpassword.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
#เตรียมลบ
# def check_credentials(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#       # return redirect('resetpassword')

#     return render(request, 'Login_Register/credentials.html')
from django.core.exceptions import MultipleObjectsReturned

def check_credentials(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=username, email=email)

            # Generate OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            
            # Send OTP via email
            send_mail(
                'รหัส OTP สำหรับการรีเซ็ตรหัสผ่าน',
                f'รหัส OTP ของคุณคือ: {otp}',
                'your-email@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['user_id_for_reset'] = user.id
            request.session['reset_email'] = email
            return redirect('verify_otp')
        
        except User.DoesNotExist:
            messages.error(request, 'Username or Email is incorrect.')
            return redirect('credentials')
        
        except MultipleObjectsReturned:
            # This handles the rare case where two user objects have the same email and username
            messages.error(request, 'พบปัญหาในระบบ, กรุณาติดต่อผู้ดูแล')
            return redirect('credentials')

    return render(request, 'Login_Register/credentials.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        # ดึง OTP จาก session ที่เราเซ็ตไว้ตอนส่งรหัสไปยังผู้ใช้
        actual_otp = request.session.get('otp')
        
        # ตรวจสอบว่า OTP ที่ผู้ใช้ป้อนเข้ามาตรงกับ OTP ใน session หรือไม่
        if entered_otp == str(actual_otp):
            # ถ้าตรง, OTP ถูกต้อง ทำกระบวนการอื่นๆต่อ
            del request.session['reset_email']
            return redirect('resetpassword')
        else:
            # ถ้าไม่ตรง, OTP ไม่ถูกต้อง
            messages.error(request, 'Incorrect OTP')
            return redirect('verify_otp')
    return render(request, 'Login_Register/verify_otp.html')


# from django.http import HttpResponse
# from django.core.mail import send_mail

# def send_email_view(request):
#     try:
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'from@example.com',
#             ['to@example.com'],
#             fail_silently=False,
#         )
#         return HttpResponse("Email sent successfully!")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")


from django.contrib.auth.forms import SetPasswordForm
def reset_password(request):
    user_id = request.session.get('user_id_for_reset')
    if user_id is not None:
        user = User.objects.get(id=user_id)
        
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                del request.session['user_id_for_reset']
                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'Login_Register/resetpassword.html', {'form': form})

    else:
        messages.error(request, 'No reset request found. Please submit your username and email again.')
        return redirect('credentials')


# logout
def logout_view(request):
    logout(request)
    return redirect('login')


def calculate_age(date_of_birth):
    if date_of_birth:
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    else:
        return 18 


@login_required
def account(request):
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user
        user_age = calculate_age(user.date_of_birth)
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth' : user.date_of_birth,
            'user_age': user_age,
            'coin' : user.coin
            if user 
            else None  # Replace with your actual field name
        } 
        return render(request, 'Account/account.html', context)
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())

#เตรียมลบ
# def update_profile(request):
#         # รับข้อมูลจากแบบฟอร์มและอัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
#         # เช่น User.objects.filter(username=request.user.username).update(first_name=new_first_name, last_name=new_last_name, email=new_email)
#         # โดยให้ new_first_name, new_last_name, และ new_email เป็นค่าที่รับจาก request.POST
#         # ตัวอย่างเท่านี้จะขึ้นอยู่กับโครงสร้างของระบบฐานข้อมูลของคุณ
#     if request.method == "POST":  #updata profile
#         user = request.user
#         profile_image = request.FILES.get('profile_image')
#         if profile_image:
#             user.image = profile_image
#             user.save()
#         return redirect('/account')  # หลังจากอัปเดตข้อมูลเรียบร้อยแล้วให้ redirect ไปยังหน้า My account หรือหน้าที่คุณต้องการ
#     return render(request, 'settingprofile.html')  # หากเป็น GET request ให้แสดงแบบฟอร์มข้อมูลแก้ไขผู้ใช้


# @login_required
# def settingprofile(request):
#     user = request.user  # Get the logged-in user
#     user_age = calculate_age(user.date_of_birth)
#     context = {
#         'username': user.username,
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'email': user.email,
#         'date_of_birth' : user.date_of_birth,
#         'user_age': user_age,
#     }
#     return render(request, 'Account/settingprofile.html', context)


@login_required
def settingprofile(request):
    user = request.user  # Get the logged-in user
    user_age = calculate_age(user.date_of_birth)

    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'date_of_birth' : user.date_of_birth,
        'user_age': user_age,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth' : user.date_of_birth.strftime('%d-%m-%Y'),
            'user_age': user_age,
        }
        return JsonResponse(data)
    else:
        return render(request, 'Account/settingprofile.html', context)


# @login_required
# def changepassword(request):
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         current_password = request.POST.get('current_password')
    #         new_password = request.POST.get('new_password')
            
    #         # ตรวจสอบว่ารหัสผ่านปัจจุบันถูกต้อง
    #         if request.user.check_password(current_password):
    #             # ตั้งรหัสผ่านใหม่และบันทึก
    #             request.user.set_password(new_password)
    #             request.user.save()
                
    #             # อัปเดตเซสชันและแจ้งให้ผู้ใช้รู้ว่ารหัสผ่านถูกเปลี่ยนแล้ว
    #             update_session_auth_hash(request, request.user)
    #             # messages.success(request, 'รหัสผ่านถูกเปลี่ยนแล้ว')
    #             return render(request, 'Account/account.html')
    #         # else:
    #             # messages.error(request, 'รหัสผ่านปัจจุบันไม่ถูกต้อง')
    #     return render(request, 'Account/changepassword.html')
    # else:
    #     template = loader.get_template('home.html')
    #     return HttpResponse(template.render())

@login_required
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password1')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'รหัสผ่านเก่าไม่ถูกต้อง')
            return redirect('changepassword')

        if new_password1 != new_password2:
            messages.error(request, 'รหัสผ่านใหม่และการยืนยันรหัสผ่านไม่ตรงกัน')
            return redirect('changepassword')

        user.set_password(new_password1)
        user.save()
        # Update session hash to keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว')
        return redirect('account')
    return render(request, 'Account/changepassword.html')# กำหนดเส้นทางของ template ที่คุณใช้


from .models import Bannerslide

# Home page
def home(request):
    slides = Bannerslide.objects.filter(active=True).order_by('order')
    movies = Movie.objects.all()
    
    movie_main_images = []

    for movie in movies:
        # ตรวจสอบและกำหนด main_image ในนี่
        main_local_image = LocalImage.objects.filter(movie=movie, mainmovie=True).first()
        if main_local_image:
            movie.main_image = main_local_image
        else:
            main_url_image = URLImage.objects.filter(movie=movie, mainmovie=True).first()
            movie.main_image = main_url_image
    # if request.user.is_authenticated:
    print(movie_main_images)
    context = {
                    'username': request.user.username,
                    'slides': slides,
                    'movies':movies,
                    'mainmovie_image':movie_main_images,
              }
    return render(request, 'home.html', context)
    # else:
        # return render(request, 'home.html', {'slides': slides})




#coin shop - ร้านค้าเหรียญ
def coinshop(request):
    premiums = Premium.objects.all()
    user = request.user

    if request.method == 'GET':
        return render(request, 'coinshop.html', {'premiums': premiums})

    if request.method == 'POST' and request.user.is_authenticated:
        premium_id = request.POST.get('premium_id')

        try:
            premium_item = Premium.objects.get(pk=premium_id)
        except Premium.DoesNotExist:
            messages.error(request, "The selected product does not exist.")
            return redirect('coinshop')
    else:
        return redirect('login')    
    with transaction.atomic():  #Transaction Handling
        if premium_item.expires < date.today():
            messages.error(request, "Sorry. this product offer has expired.")
            return redirect('coinshop')

        elif premium_item.num <= 0:
            messages.error(request, "Sorry. this product is out of stock.")
            return redirect('coinshop')

        if request.user.coin >= premium_item.price:
            request.user.coin -= premium_item.price
            request.user.save()

            premium_item.num -= 1
            premium_item.save()

            # Record the purchase
            Premium_list.objects.create(user=request.user, premium=premium_item)
            subject = 'ขอบคุณที่ทำการซื้อสินค้าที่เรา'
            message = f'สวัสดีคุณ {user.username},\n\n'\
                    f'ขอบคุณที่ทำการซื้อสินค้า\n'\
                    'รายการสินค้า\n'\
                    f'"{premium_item.name}" ในราคา {premium_item.price} coins.\n'\
                    'หากมีข้อสงสัยหรือปัญหาเกี่ยวกับสินค้า กรุณาติดต่อเราได้ที่ Blueeye.or@gmail.com\n\n'\
                    'ด้วยความนับถือ,\n'\
                    'ทีมงาน MovieReview'
            from_email = 'your-email@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Purchase successful!")
        else:
            messages.error(request, "Not enough coins!")

    context = {
        'premiums': premiums
    }
    if request.user.is_authenticated:
        context.update({
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'coin': request.user.coin,
        })
        
    return render(request, 'coinshop.html', context)


from django.db.models import Avg
def moviereview(request, id):
    movie = get_object_or_404(Movie, pk=id)
    form = CommentForm(request.POST)  # Instantiate the form for POST; None will make it unbound for GET
    user = request.user # User
    directors = movie.director.all()
    writers = movie.writer.all()
    # directors = movie.director.all().values_list('id')  # ตัวอย่าง: เลือกเฉพาะชื่อและ ID
    # writers = movie.writer.all().values_list('id')
    top_stars = MovieDetail.objects.filter(movie=movie, is_top=True)
    # movie_details = MovieDetail.objects.all()

    # for detail in movie_details:
    #     star = detail.star
    #     # ตรวจสอบ LocalImage ที่เป็น mainstar
    #     local_images = LocalImage.objects.filter(star=star, mainstar=True)
        
    #     if local_images.exists():
    #         detail.image = local_images.first().image.url
    #     else:
    #         # ถ้าไม่มี LocalImage, ใช้ URLImage
    #         url_images = URLImage.objects.filter(star=star)
    #         if url_images.exists():
    #             detail.image_url = url_images.first().image_url

    top_star_images = []  # ใช้ list เพื่อเก็บ URL ของรูปภาพ
    for star_detail in top_stars:
        star = star_detail.star  # ดึง object ของ Star

        # ตรวจสอบ LocalImage ที่เป็น mainstar
        local_images = LocalImage.objects.filter(star=star, mainstar=True)
        
        if local_images.exists():
            # ถ้ามี LocalImage
            image_url = local_images.first().image.url
        else:
            # ถ้าไม่มี LocalImage, ใช้ URLImage
            url_images = URLImage.objects.filter(star=star, mainstar=True)
            if url_images.exists():
                # ถ้ามี URLImage
                image_url = url_images.first().image_url
            else:
                # ถ้าไม่มีทั้ง LocalImage และ URLImage
                image_url = None
        top_star_images.append(image_url)
    print(top_star_images)



    if request.user.is_authenticated :  # Check if the user is authenticated
        commented = Comment.objects.filter(movie=movie, user=user).first()
        other_comments = Comment.objects.filter(movie=movie).exclude(user=user)
        print(commented)
    else:
        commented = None
        other_comments = Comment.objects.filter(movie=movie).exclude() 
    
    # comment_id = request.POST.get('comment_id')
    # print(comment_id)
    # Aggregate the total score for the movie
    avg_score_result = Comment.objects.filter(movie=movie).aggregate(average_score=Avg('score'))
    avg_score = avg_score_result.get('average_score',0)

    if avg_score is not None:
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0
    # If there are no comments yet, average_score will be None
    # if average_score is None:
    #     average_score = 0

    if request.method == 'POST':
        if commented:  # ตรวจสอบว่าผู้ใช้แสดงความคิดเห็นแล้วหรือไม่
            form = CommentForm(request.POST, instance=commented)  # ใช้ CommentForm ผูกกับความคิดเห็นที่มีอยู่แล้ว
        else:
            form = CommentForm(request.POST)     #ไม่มีความคิดเห็นที่มีอยู่ สร้างความคิดเห็นใหม่ 

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            return redirect('moviereview', id=id)

    if request.method == 'GET':
        try:
            video = get_object_or_404(Video, movie=movie)
        except:
            video = None

        # Images main movie
        mainmovie_image = None
        local_mainmovie_image = LocalImage.objects.filter(is_visible=True, mainmovie=True, movie=movie)
        url_mainmovie_image = URLImage.objects.filter(is_visible=True, mainmovie=True, movie=movie)

        if local_mainmovie_image.exists():
            mainmovie_image = local_mainmovie_image.first()
        elif url_mainmovie_image.exists():
            mainmovie_image = url_mainmovie_image.first()

        # Image movie
        local_images = LocalImage.objects.filter(is_visible=True, movie=movie, mainmovie=0)
        url_images = URLImage.objects.filter(is_visible=True, movie=movie, mainmovie=0)
        movie_images = list(local_images) + list(url_images)

        # ดึงรูปภาพจาก LocalImage และ URLImage ที่เป็น mainstar สำหรับ star นี้
        # movie_details = MovieDetail.objects.select_related('star', 'movie').all()
        # for detail in movie_details:
        #     print(f"{detail.star.name} - {detail.character_name} in {detail.movie.name}")
        # mainstar_local_images = LocalImage.objects.filter(mainstar=True)
        # if not mainstar_local_images.exists():
        #     mainstar_url_images = URLImage.objects.filter(mainstar=True)
        #     for image in mainstar_url_images:
        #         print(f"Image URL: {image.image_url}")
        #         stars = ', '.join(star.name for star in image.star.all())
        #         print(f"Stars: {stars}")
        # else:
        #     for image in mainstar_local_images:
        #         print(f"Image URL: {image.image.url}")
        #         stars = ', '.join(star.name for star in image.star.all())
        #         print(f"Stars: {stars}")

        context = {
            'movie': movie,
            'user': user,
            'scoreAvg':avg_score,
            'directors':directors,
            'writers':writers,
            'topcast': top_stars,
            # 'top_star_images': top_star_images,
            # 'movie_details': movie_details,
            'star_images':top_star_images,
            'mainmovie_image': mainmovie_image,
            'movie_image': movie_images,
            'video': video,
            'form': form,  # Include form in GET context
            'commented':commented,
            'other_comments':other_comments,

            # ===================
            # 'mainstar_local_images': mainstar_local_images,
            # 'mainstar_url_images': mainstar_url_images,
            # 'movie_details': movie_details,
            
        }
        return render(request, 'moviereview.html', context)
    return render(request, 'moviereview.html', context)




# @require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        # If like already exists, it means user is unliking the comment
        like.delete()
        is_liked = False
    else:
        is_liked = True

    # Check for AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"is_liked": is_liked, "comment_id": comment_id})
    print(is_liked)
    # Redirect for non-AJAX request
    return redirect('moviereview', '1')  # Adjust the redirect as needed


def actor(request, id):
    # search_query = request.GET.get('search', None)
    # star = Star.objects.filter(name__icontains=search_query) # ฟังชัน icontains สตริง โดยไม่คำนึงถึงตัวพิมพ์เล็กและตัวพิมพ์ใหญ่
    star = get_object_or_404(Star, pk=id)
    startype = [job.name for job in star.job.all()]
    height  = '{:.1f}'.format(star.height * 3.28084)
    official_list = star.official_sites_set.all()
    alternative_names = AlternativeNames.objects.filter(star=star)
    relatives = Relatives.objects.filter(star=star)
    other_works = OtherWorks.objects.filter(star=star)
    # Born
    born_date = star.born_date
    born_location = star.born_location
    # Died
    died_date = star.died_date
    died_location = star.died_location
    # Spouse
    spouse = Spouses.objects.filter(star=star)
    # spouse_to_others = star.spouse_star.all()
    # Children
    children_of_star = Children.objects.filter(star=star)
    children = [child.child_name for child in children_of_star if child.child_name is not None]
    # Parent
    parent_relations = Children.objects.filter(child_name=star)
    parent_names = [relation.star.name for relation in parent_relations]

    # ดึงรูปภาพจาก LocalImage และ URLImage ที่เป็น mainstar สำหรับ star นี้
    mainstar_image = None
    local_mainstar_image = LocalImage.objects.filter(is_visible=True, mainstar=True, star=star)
    url_mainstar_image = URLImage.objects.filter(is_visible=True, mainstar=True, star=star)

    if local_mainstar_image.exists():
        mainstar_image = local_mainstar_image.first()
    elif url_mainstar_image.exists():
        mainstar_image = url_mainstar_image.first()
    # Image
    local_images = LocalImage.objects.filter(is_visible=True, star=star, mainstar=0)
    url_images = URLImage.objects.filter(is_visible=True, star=star, mainstar=0)

    # You may want to combine them into one list if they are treated similarly in the template
    non_mainstar_images = list(local_images) + list(url_images)
    
    context = {
        'star': star,
        'jobs_list': startype,
        'height':height,
        'official_list':official_list,
        'mainstar_image':mainstar_image,
        'alternative_names':alternative_names,
        'relatives':relatives,
        'other_works':other_works,
        'born_date':born_date,
        'born_location':born_location,
        'died_date':died_date,
        'died_location':died_location,
        'spouse':spouse,
        # 'spouse_to_others':spouse_to_others,
        'children':children,
        'parent':parent_names,
        'non_mainstar_images':non_mainstar_images,
    }
    return render(request, 'actor.html',context)


from django.conf import settings
from django.shortcuts import redirect

# 404 page 
def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_view(request):
    
    context = {
    }
    
    return render(request, 'admin/dashboard.html', context)


#admin custom view
# my_custom_view