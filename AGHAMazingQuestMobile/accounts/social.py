from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class GoogleLogin(SocialLoginView):
    """Endpoint to accept a Google token from mobile clients and return JWTs.

    Mobile apps should POST {"access_token": "<GOOGLE_ACCESS_TOKEN>"}
    to this endpoint. dj-rest-auth + allauth will handle creating or linking
    the user and dj-rest-auth will return JWT `access` and `refresh` tokens.
    """

    adapter_class = GoogleOAuth2Adapter
