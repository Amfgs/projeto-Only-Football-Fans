from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta é a única linha de 'include' que você precisa, 
    # já que o 'core.urls' cuida de todo o resto.
    path('', include('core.urls')), 
]

# --- CORREÇÃO DA MÍDIA (Ainda necessária) ---
# Isso permite que o 'runserver' encontre suas imagens locais.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)