
from rest_framework import viewsets
from .models import Video, VideoFile
from .serializers import VideoSerializer
from rest_framework.response import Response
from django.http import FileResponse

class VideoView(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset
    
class VideoHLSView(viewsets.ViewSet):
    """View to serve HLS playlist and segments for a video."""
    def retrieve(self, request,movie_id, resolution):
        try:
            video_file = VideoFile.objects.get(video=movie_id, resolution=resolution)
            path = f"{video_file.hls_path}/index.m3u8"
            return FileResponse(open(path, 'rb'), content_type='application/vnd.apple.mpegurl')
        except VideoFile.DoesNotExist:
            return Response({'error': 'Video file not found'}, status=404)

class VideoHLSSegmentView(viewsets.ViewSet):
    """View to serve HLS segments for a video."""
    def retrieve(self, request,movie_id, resolution, segment):
        try:
            video_file = VideoFile.objects.get(video=movie_id, resolution=resolution)
            path = f"{video_file.hls_path}/{segment}"
            return FileResponse(open(path, 'rb'), content_type='video/MP2T')
        except VideoFile.DoesNotExist:
            return Response({'error': 'Video file not found'}, status=404)