from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from adminapp.models import CustomUser



class CheckAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/superuser') or request.path.startswith('/admin'):
            if not request.user.is_authenticated or not request.user.is_superuser:
                return HttpResponseRedirect(reverse('h_index'))
            
        elif request.path.startswith('/web'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('h_index'))
            else:    
                if request.user.is_superuser and request.user.is_staff:
                    return HttpResponseRedirect(reverse('h_index'))
                else:
                    user = CustomUser.objects.get(user_ptr_id=request.user.pk)
                    if not user.is_manager and not user.is_worker:  
                        return HttpResponseRedirect(reverse('h_index'))
                
        return self.get_response(request)