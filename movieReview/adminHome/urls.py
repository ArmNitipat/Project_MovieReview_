from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import calendarscraper

#------------------------------------------------------------------------------------
# from .views import send_my_email
from django.contrib.auth import views as auth_views
#------------------------------------------------------------------------------------
handler404 = 'adminHome.views.error_404_view'

urlpatterns = [
    path('',views.home, name='home'),
    path('search/', views.search, name='search'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.signup_view, name='register'),
    path('account/',views.account, name='account'),
    path('settingprofile/',views.settingprofile, name='settingprofile'),
    path('update_user/', views.update_user, name='update_user'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('credentials/', views.check_credentials, name='credentials'),
    path('resetpassword/', views.reset_password, name='resetpassword'),
    path('moviereview/<int:id>/', views.moviereview, name='moviereview'),
    path('actor/<int:id>/', views.actor, name='actor'),
    path('coinshop/', views.coinshop, name='coinshop'),
    path('calender/', calendarscraper, name='calender'),
    path('minigame/', views.minigame, name='minigame'),
    path('updatecoin/', views.updatecoin, name='updatecoin'),
    path('update_session/', views.update_session, name='update_session'),
    path('about_us/', views.about_us, name='about_us'),
    path('calender/<int:year>/<int:month>/', views.calendarscraper, name='calender'),
    path('calendarTH/', views.calendarTH, name='calendarTH'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    #admin
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('scraping/', views.scraping_view, name='scraping'),
    path('scraping/movie/<str:name>/', views.scraping_Movie, name='scraping_Movie'),
    path('scraping/actor/<str:name>/', views.scraping_Actor, name='scraping_Actor'),
    path('scraping/movie/scrapingsave/<str:name>', views.scraping_movie_save, name='scraping_movie_save'),
    path('scraping/actor/scrapingsave/<str:name>', views.scraping_actor_save, name='scraping_actor_save'),
    path('search_api/', views.search_api, name='search_api'),
    path('search_admin/', views.search_admin, name='search_admin'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # path('send_my_email/', send_my_email, name='send_my_email'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    # re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('check_email/', views.check_email, name='check_email'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('report_comment/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('scrape_movie_data/<str:movie>/', views.scrape_movie_data, name="scrape_movie_data"),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # path('my_custom_view/', views.my_custom_view, name='my_custom_view')
    path('test/', views.test, name='test'),
    path('scrapingmovie/', views.scraping_Movie, name = 'scraping_movieTest'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
]    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

# handler404 == 'adminHome.views.handler404'