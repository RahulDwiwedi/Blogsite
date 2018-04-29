"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from posts import views

urlpatterns = [
    url(r'^$',views.post_list),
    url(r'^login/',views.user_login),
    url(r'^auth/', views.auth_view),
    url(r'^dashboard/', views.dashboard),
    url(r'^submit-post/', views.post_submittion),
    url(r'^logout/', views.logout),
    url(r'^post/(?P<id>\d+)/$', views.singlepost),
    url(r'^post/(?P<id>\d+)/edit$', views.post_edit),
    url(r'^post/(?P<id>\d+)/delete$', views.post_delete),
    url(r'^user/(?P<id>\d+)/$', views.author),
    url(r'^register_success/', views.register_success),
    url(r'^user/edit$', views.user_profile_edit),
    url(r'^user_registration/', views.user_registration, name="user_registration"),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
