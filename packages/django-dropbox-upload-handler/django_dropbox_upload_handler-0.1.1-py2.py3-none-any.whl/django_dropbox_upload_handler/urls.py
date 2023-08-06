from django.conf.urls import url
from .views import UploadProgressView

urlpatterns = [
    url(r'^upload_progress$', UploadProgressView.as_view())
]
