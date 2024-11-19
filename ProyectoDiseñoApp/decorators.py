from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin', False):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('/Principal/')
        return view_func(request, *args, **kwargs)
    return wrapper
