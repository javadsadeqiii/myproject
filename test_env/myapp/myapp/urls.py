"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from rest_framework import routers
from blog import views


router = routers.DefaultRouter()
router.register(r'userRegister',views.userRegisterViewSet)
router.register(r'userLogin',views.userLoginViewSet) 
router.register(r'updateUsername',views.updateUsernameViewSet)
router.register(r'updatePassword',views.updatePasswordViewSet)
router.register(r'comments',views.commentsViewSet)
router.register(r'commentsLike',views.commentsLikeViewSet)
router.register(r'allPosts', views.allPostsViewSet)
router.register(r'authors', views.authorsViewSet)
router.register(r'wallpapers',views.wallpapersViewSet)
router.register(r'albums', views.albumsViewSet)
router.register(r'soundTracks', views.soundTracksViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),

    
    
]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)




