from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
import os

from .api.views import index_view, MessageViewSet
from .takers.views.user import UserViewSet, CustomObtainAuthToken
from .takers.views.giver import GiverViewSet
from .takers.views.taker import TakerViewSet
from .takers.views.donate import DonateViewSet
from .takers.views.image import ImageViewSet
from .takers.views.city import CityViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('messages', MessageViewSet)
router.register('givers', GiverViewSet, basename='Giver')
router.register('takers', TakerViewSet, basename='Taker')
router.register('donates', DonateViewSet)
router.register('images', ImageViewSet, basename='Image')
router.register('cities', CityViewSet)

urlpatterns = [
    # http://localhost:8090/
    path('', index_view, name='index'),

    path('docs/', include_docs_urls(title='Api Points')),

    # http://localhost:8090/api/admin/
    path('admin/', admin.site.urls),

    #path(r'^logout/$', views.logout_user, name='logout'),
    path('api/auth/', CustomObtainAuthToken.as_view(), name='get_auth_token'),

    # http://localhost:8090/api/<router-viewsets>
    path('api/', include(router.urls)),
]

baseDir = settings.BASE_DIR + os.sep
images = settings.MEDIA_URL.replace('/', '')
imgsDir = os.path.join(os.sep, baseDir, images)
urlpatterns += static('images/', document_root=imgsDir)
