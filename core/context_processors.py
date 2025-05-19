from .models import Core

def core(request):
    core = Core.objects.all().first() if Core.objects.all() else ''

    return {
        'core': core,
    }
