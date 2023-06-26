from django.contrib.auth.models import Group


class GroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        if user.is_authenticated:
            group = None
            try:
                group = Group.objects.get(user=user)
            except Group.DoesNotExist:
                pass
            request.user_group = group
        return response
