from functools import wraps
from django.core.exceptions import PermissionDenied


ADMIN_ROLES = ['super_admin', 'principal']
TEACHER_ROLES = ['super_admin', 'principal', 'teacher']
ALL_ROLES = ['super_admin', 'principal', 'teacher', 'student', 'parent']


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
