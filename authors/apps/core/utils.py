from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


class Utilities:
    """Utility class that contains helper function"""

    @staticmethod
    def email_renderer(data):
        """This function sends email to users."""

        url = f"http://{get_current_site(data[0]).domain}\
            /api/users/{data[1]}?token={data[2]}"
        subject = f"[Authors Heaven] {data[3]}"
        body = f"Hello, \
                \nYou are receiving this e-mail because you have {data[4]}' \
                 '\nClick the click below to verify your account.\n{url}"
        EmailMessage(subject, body, to=[data[5]]).send(fail_silently=False)
        return
