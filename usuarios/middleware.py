import threading


_user = threading.local()


class CurrentUserMiddleware:
    """Middleware to store the current user in thread-local storage."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = getattr(request, "user", None)  # Store user
        response = self.get_response(request)
        return response


def get_current_user():
    """Retrieve the stored user in signals."""
    return getattr(_user, "value", None)
