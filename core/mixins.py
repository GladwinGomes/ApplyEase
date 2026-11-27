"""
Custom view mixins for ApplyEase.
"""

from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin that restricts access to users with the 'admin' role.
    Redirects to login page if the test fails.
    """

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and getattr(self.request.user, 'role', None) == 'admin'
        )
