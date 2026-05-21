from rest_framework.routers import DefaultRouter
from .views import VideoView, VideoHLSView, VideoHLSSegmentView
from django.urls import path, include

router = DefaultRouter()
router.register(r'video', VideoView)

urlpatterns = [
    path('', include(router.urls)),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoHLSView.as_view({'get': 'retrieve'})),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoHLSSegmentView.as_view({'get': 'retrieve'})),
]