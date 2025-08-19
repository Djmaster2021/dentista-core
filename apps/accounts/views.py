from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class RoleLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("portal:dentist_home") if getattr(user, "role", "") == "DENTIST" else reverse_lazy("portal:patient_home")
