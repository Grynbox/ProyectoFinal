from django.contrib.auth.decorators import login_required
from .models import UsuarioAutocar

def user_info(request):
    if request.user.is_authenticated:
        return {
            'departamento_usuario': request.user.departamento,  # Asumiendo que tienes un campo departamento en tu modelo de usuario.
            'usuario_logueado': request.user.username
        }
    return {}