from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.cache import cache

class UploadProgressView(View):
    def get(self, request, *args, **kwargs):
        progress_id = ''
        if 'progress_id' in request.GET:
            progress_id = request.GET['progress_id']
        elif 'progress_id' in request.META:
            progress_id = request.META['progress_id']
        if progress_id:
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            if data is None:
                return HttpResponse(status=201)
            return JsonResponse({'uploaded': data['uploaded'], 'length': data['length']})
        else:
            return HttpResponse(status=400)
