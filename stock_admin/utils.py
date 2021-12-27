import threading

import mailchimp
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from users.models import User


class SendSubscribeMail(object):
    def __init__(self, email, first_name=None, last_name=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        API_KEY = settings.MAILCHIMP_API_KEY
        LIST_ID = settings.MAILCHIMP_SUBSCRIBE_LIST_ID
        api = mailchimp.Mailchimp(API_KEY)
        merge_vars = {"FNAME": self.first_name, "LNAME": self.last_name}
        try:
            if self.first_name and self.last_name and self.email:
                api.lists.subscribe(LIST_ID, {"email": self.email}, merge_vars)
            else:
                api.lists.subscribe(LIST_ID, {"email": self.email})
        except:
            return False


def get_current_users():
    """Return list of all active users."""
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get("_auth_user_id", None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)
