from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse


class SuperuserCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            response = self.get_response(request)
        else:
            if not request.path.startswith('/superuser') and not request.path.startswith('/admin'):
                response = self.get_response(request)
            else:
                response = HttpResponseRedirect(reverse('h_index'))
        return response


class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_active:
            response = self.get_response(request)
        else:
            if not request.path.startswith('/web'):
                response = self.get_response(request)
            else:
                response = HttpResponseRedirect(reverse('h_index'))
        return response

