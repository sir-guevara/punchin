# Generated by Django 5.0.2 on 2024-02-26 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_shift_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='organizaiton',
            new_name='organization',
        ),
    ]