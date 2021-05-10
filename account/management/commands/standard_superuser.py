import logging

from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import BaseCommand
from account.models import MyAccountManager
from account.models import Account

GROUPS = ['laborant', 'admin', 'superadmin']
PERMISSIONS = ['Can add/edit/delete sampling',]


class Command(BaseCommand):
    help = 'Creates read only default superadmin account'

    def handle(self, *args, **options):
        Account.object.create_superuser(username="admin", first_name="Administrator_first_name",
                                        last_name='Administrator_last_name', password='admin12345', must_change_password=True)
        print("Created default superuser.")