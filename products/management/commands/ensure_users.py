"""
Management command: ensure_users
Creates the default admin and staff users if they don't exist.
Safe to run multiple times — uses get_or_create and always sets the password.
"""
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Ensures default admin and staff users exist with correct passwords.'

    def handle(self, *args, **options):
        # ── Admin ─────────────────────────────────────────────────────────────
        admin, created = User.objects.get_or_create(
            username='Nandhan',
            defaults={
                'email': 'nandhan@retailpos.com',
                'first_name': 'Nandhan',
                'last_name': 'K',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        admin.role = User.Role.ADMIN
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.set_password('admin123')
        admin.save()
        self.stdout.write(self.style.SUCCESS(
            f"{'Created' if created else 'Updated'} admin: Nandhan / admin123"
        ))

        # ── Staff accounts ─────────────────────────────────────────────────────
        staff_data = [
            ('bins_7',    'Bins',     'Mathew', 'bins@retailpos.com'),
            ('Akhil',     'Akhil',    'Raj',    'akhil@retailpos.com'),
            ('Syamjith',  'Syamjith', 'S',      'syamjith@retailpos.com'),
            ('Susmitha',  'Susmitha', 'P',      'susmitha@retailpos.com'),
        ]
        for username, first, last, email in staff_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                    'role': User.Role.STAFF,
                    'is_staff': False,
                    'is_active': True,
                }
            )
            user.role = User.Role.STAFF
            user.is_active = True
            user.set_password('staff123')
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} staff: {username} / staff123"
            ))
