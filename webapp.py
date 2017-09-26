from datetime import date
from os import environ

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.conf.urls import url
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import RedirectView, View

from scraper import get_screenings


settings.configure(
    DEBUG=environ.get('DEBUG'),
    ALLOWED_HOSTS=['*'],
    ROOT_URLCONF=__name__,
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': 60 * 60 * 2,
        }
    }
)


class JSONView(View):
    def dispatch(self, request, **kwargs):
        resp = JsonResponse(self.get_api_stuff(**kwargs))
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


class OdeonTimesView(JSONView):
    def get_api_stuff(self, odeon_id):
        cache_key = 'odeon:{}:{}'.format(odeon_id, date.today().isoformat())
        hit = cache.get(cache_key)

        if hit is not None:
            return hit

        rv = {
            'status': 'ok',
            'listings': get_screenings(odeon_id),
        }

        cache.set(cache_key, rv)
        return rv


urlpatterns = [
    url(r'^odeon/(?P<odeon_id>\d+)/$', OdeonTimesView.as_view()),
    url(r'^', RedirectView.as_view(
        url='https://github.com/colons/odeon-scraper'
    )),
]


application = get_wsgi_application()


if __name__ == '__main__':
    import sys

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
