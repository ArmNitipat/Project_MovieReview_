# Generated by Django 4.2.5 on 2023-11-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminHome', '0015_comment_update_date_alter_comment_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='spoiler',
            field=models.BooleanField(),
        ),
    ]
