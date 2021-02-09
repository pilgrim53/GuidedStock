from celery import shared_task


@shared_task
def summary():
    print('Hello Pritesh')
