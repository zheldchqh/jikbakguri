# Generated by Django 5.2.1 on 2025-05-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0009_comment_modify_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
