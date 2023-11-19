# Generated by Django 4.2.5 on 2023-11-13 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_movie_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localimage',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_images_movie', to='movies.movie'),
        ),
        migrations.AlterField(
            model_name='urlimage',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='url_movie_images', to='movies.movie'),
        ),
    ]
