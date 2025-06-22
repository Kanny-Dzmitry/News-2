from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import News

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create groups if they don't exist
        common_group, created = Group.objects.get_or_create(name='common')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "common" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Group "common" already exists'))

        authors_group, created = Group.objects.get_or_create(name='authors')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "authors" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Group "authors" already exists'))

        # Get content type for News model
        news_content_type = ContentType.objects.get_for_model(News)

        # Get permissions for News model
        add_news_permission = Permission.objects.get(
            content_type=news_content_type,
            codename='add_news'
        )
        change_news_permission = Permission.objects.get(
            content_type=news_content_type,
            codename='change_news'
        )
        delete_news_permission = Permission.objects.get(
            content_type=news_content_type,
            codename='delete_news'
        )

        # Assign permissions to authors group
        authors_group.permissions.add(
            add_news_permission,
            change_news_permission,
            delete_news_permission
        )
        self.stdout.write(self.style.SUCCESS('Permissions assigned to "authors" group successfully')) 