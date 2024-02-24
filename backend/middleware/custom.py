from django.http import HttpResponseNotAllowed


def methods_only(*methods: str):
    methods = [m.upper() for m in methods]
    def wraps(func):
        def middleware(request):
            if request.method not in methods:
                return HttpResponseNotAllowed(methods)
            return func(request)
        return middleware
    return wraps
