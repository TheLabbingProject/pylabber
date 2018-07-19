from .models import Study


def db(request):
    return {'studies': Study.objects.all()}
