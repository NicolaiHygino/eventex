from django.conf.urls import include, url

from eventex.subscriptions.views import new, detail

app_name = 'subscriptions'

urlpatterns = [
    url(r'^$', new, name='new'),
    url(r'^(\w+)/$', detail, name='detail'),
]
