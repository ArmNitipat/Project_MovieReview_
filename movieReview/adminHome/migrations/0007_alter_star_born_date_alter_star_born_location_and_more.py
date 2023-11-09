# Generated by Django 4.2.5 on 2023-10-30 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminHome', '0006_official_sites_startype_remove_actor_star_ptr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star',
            name='born_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='star',
            name='born_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='star',
            name='died_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='star',
            name='died_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='star',
            name='height',
            field=models.FloatField(blank=True, default=0, help_text='height in meters.'),
        ),
    ]