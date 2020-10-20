from .models import Log


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.method == "POST":
            log = Log.objects.create(message=request.POST)
            log.save()

        if request.method == "GET":
            log = Log.objects.create(message=request.GET)
            log.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
