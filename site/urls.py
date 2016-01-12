from django.conf.urls import include, url
from django.contrib import admin

import bookshelf.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bookshelf/', include(bookshelf.urls, namespace='bookshelf')),
]
