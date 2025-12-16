from django.http import JsonResponse
from django.views import View


class APIRootView(View):
    """Small API root that lists the available auth-related endpoints.

    This is useful during development so a request to `/api/` doesn't return 404.
    """

    def get(self, request, *args, **kwargs):
        endpoints = {
            'auth': request.build_absolute_uri('/api/auth/'),
            'registration': request.build_absolute_uri('/api/auth/registration/'),
            'google': request.build_absolute_uri('/api/auth/google/'),
            'profile': request.build_absolute_uri('/api/auth/profile/'),
            'otp_request': request.build_absolute_uri('/api/auth/otp/request/'),
            'otp_verify': request.build_absolute_uri('/api/auth/otp/verify/'),
            'admin': request.build_absolute_uri('/admin/'),
        }
        return JsonResponse({'api_root': endpoints})
