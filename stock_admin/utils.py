import threading

import mailchimp
from django.conf import settings


class SendSubscribeMail(object):
    def __init__(self, email , first_name=None,last_name=None):
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
        merge_vars = {
            "FNAME": self.first_name,
            "LNAME": self.last_name
        }
        try:
            if self.first_name and self.last_name and self.email:
                api.lists.subscribe(
                    LIST_ID, {"email": self.email}, merge_vars)
            else:
                api.lists.subscribe(LIST_ID, {"email": self.email})
        except:
            return False
