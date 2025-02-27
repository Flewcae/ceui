from django.http import JsonResponse
from functools import wraps
from user.models import CustomUser

def perm_required(action_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                print('user bulunamadı')
                return JsonResponse({'message': 'Oturum açmanız gerekmektedir.'}, status=403)
            
            user_group = user.groups.first()

            if not user_group:
                print('user group bulunamadı')
                return JsonResponse({'message': 'Oturum açmanız gerekmektedir.'}, status=403)

            is_allowed = user_group.permissions.filter(codename = action_name).exists()

            if is_allowed:
                return view_func(request, *args, **kwargs)
            else:
                print('user yetkisi bulunamadı')
                return JsonResponse({'message': 'Bu sayfaya erişim yetkiniz bulunmamaktadır.'}, status=403)
        return _wrapped_view
    return decorator
