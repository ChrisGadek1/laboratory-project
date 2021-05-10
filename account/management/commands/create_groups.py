import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['laborant', 'admin', 'superadmin']
PERMISSIONS = ['Can add/edit/delete sampling', 'Can add/edit/delete WIJHARS', 'Can add/edit/delete ControlType',
                'Can add/edit/delete MetodAndNorm', 'Can add/edit/delete Type', 'Can add/edit/delete DeliveryWay',
                'Can add/edit/delete ResearchStatus',  'Can add/edit/delete Research',
               ]


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for permission in PERMISSIONS:
                try:
                    model_add_perm = Permission.objects.get(name=permission)
                except Permission.DoesNotExist:
                    logging.warning("Permission not found with name '{}'.".format(permission))
                    continue

                new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")