# Generated by Django 2.1.7 on 2019-06-09 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='singer',
            new_name='singers',
        ),
    ]