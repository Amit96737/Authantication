from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def sub_admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and (getattr(request.user, 'is_sub_admin', False) or request.user.is_staff):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_sign_up')
    return _wrapped_view_func
