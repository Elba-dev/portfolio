from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from pathlib import Path

# Root directory of the portfolio project (parent of the backend folder)
PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent.parent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contact.urls')),
    
    # Serve static assets (js, css, images) from the portfolio root
    re_path(r'^(?P<path>(js|css|images)/.*)$', serve, {'document_root': PORTFOLIO_ROOT}),
    
    # Serve individual HTML files
    re_path(r'^(?P<path>.*\.html)$', serve, {'document_root': PORTFOLIO_ROOT}),
    
    # Serve index.html at root url
    path('', serve, {'document_root': PORTFOLIO_ROOT, 'path': 'index.html'}),
]
