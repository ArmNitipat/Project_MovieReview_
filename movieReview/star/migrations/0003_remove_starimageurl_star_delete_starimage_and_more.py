# Generated by Django 4.2.5 on 2023-10-31 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0002_startype_star_active_star_born_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='starimageurl',
            name='star',
        ),
        migrations.DeleteModel(
            name='StarImage',
        ),
        migrations.DeleteModel(
            name='StarImageURL',
        ),
    ]
