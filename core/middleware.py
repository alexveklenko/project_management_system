from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if path != '/login/' and path != '/register/' and not path.startswith('/password-reset/') and not path.startswith('/admin/'):
                return redirect('/login/?next=%s' % path)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
