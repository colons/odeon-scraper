from os import environ

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.conf.urls import url
from django.http import JsonResponse
from django.views.generic import View

from scraper import get_screenings


settings.configure(
    DEBUG=environ.get('DEBUG'),
    ALLOWED_HOSTS=['*'],
    ROOT_URLCONF=__name__,
)


class JSONView(View):
    def dispatch(self, request, **kwargs):
        return JsonResponse(self.get_api_stuff(**kwargs))


class OdeonTimesView(JSONView):
    def get_api_stuff(self, odeon_id):
        return {
            'status': 'ok',
            'listings': get_screenings(odeon_id),
        }


urlpatterns = [
    url(r'^odeon/(?P<odeon_id>\d+)/$', OdeonTimesView.as_view()),
]


application = get_wsgi_application()


if __name__ == '__main__':
    import sys

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
