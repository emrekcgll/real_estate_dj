from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse


class SuperuserCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            response = self.get_response(request)
        else:
            if not request.path.startswith('/superuser') and not request.path.startswith('/admin') :
                response = self.get_response(request)
            else:
                if request.user.groups.filter(name="Admin"):
                    response = HttpResponseForbidden("401 Unauthorized!")
                else:
                    response = HttpResponseRedirect(reverse('h_index'))
        return response


class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name="Admin") \
            or request.user.is_superuser:
            response = self.get_response(request)
        else:
            if not request.path.startswith('/web'):
                response = self.get_response(request)
            else:
                # response = HttpResponseForbidden("401")
                response = HttpResponseRedirect(reverse('h_index'))
        return response

