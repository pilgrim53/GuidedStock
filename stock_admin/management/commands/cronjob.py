from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import IntervalSchedule, PeriodicTask, SECONDS


class Command(BaseCommand):
    help = 'Setup cronjob for updating stock data.'

    def handle(self, *args, **options):
        if PeriodicTask.objects.filter(task='stock_admin.tasks.update_stock_prices').exists():
            self.stdout.write(self.style.SUCCESS('Cronjob is already set!!'))
        else:
            schedule = IntervalSchedule.objects.create(every=1, period=SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='Update Stocks',
                task='stock_admin.tasks.update_stock_prices')
            task.enabled = True
            task.save()
            self.stdout.write(self.style.SUCCESS(
                'Cronjob successfully setup!!'))
