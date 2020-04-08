"""Elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
from courses.views import course_detail, course_list, do_section,do_test,show_results,home,section_instructions,all_result
from accounts.views import login,signup

urlpatterns = [
    path('',home,name='home'),
    path('login',login,name='login'),
    path('signup',signup,name='signup'),
    path('socialaccounts/',include('allauth.urls')),
    path('course_list', course_list, name='course_list'),
    path('all_result/<int:course_id>',all_result,name='all_result'),
    path('instructions/<int:section_id>/',section_instructions,name='section_instructions'),
    path('section/<int:section_id>/test/',do_test,name='do_test'),
    path('section/<int:section_id>/',do_section,name='do_section'),
    path('course_detail/<int:course_id>/', course_detail, name='course_detail'),
    path('section/<int:section_id>/results/',show_results,name='show_results'),
    path('admin/', admin.site.urls),
]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
