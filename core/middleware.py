from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/dashboard/' and not request.user.is_authenticated:
            return redirect('user_login')

        response = self.get_response(request)
        return response