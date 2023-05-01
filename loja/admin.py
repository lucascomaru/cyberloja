from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Produto, UsuarioPersonalizado
# Register your models here.
class UsuarioAdmin(UserAdmin):
    list_display = ('nome', 'email', 'telefone')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('nome', 'email', 'telefone')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)
admin.site.register(Produto)
admin.site.register(UsuarioPersonalizado, UsuarioAdmin)
