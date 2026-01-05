from allauth.account.adapter import DefaultAccountAdapter

class NoEmailVerificationAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Disable allauth confirmation emails completely
        return
