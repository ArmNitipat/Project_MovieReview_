# Generated by Django 4.2.5 on 2023-10-30 07:01

from django.db import migrations, models
import django.db.models.deletion
import movies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminHome', '0007_alter_star_born_date_alter_star_born_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Movie Name')),
                ('release_date', models.DateField(verbose_name='Movie Release Date')),
                ('story', models.TextField()),
                ('time', models.TimeField(verbose_name='Movie Time')),
                ('is_show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MovieRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MovieTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Video Title')),
                ('video_url', models.URLField(verbose_name='Video URL')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_videos', to='movies.movie')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_videos', to='adminHome.star')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.CreateModel(
            name='URLImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(verbose_name='Image URL')),
                ('is_main', models.BooleanField(default=False, verbose_name='Is Main')),
                ('is_visible', models.BooleanField(default=True, null=True, verbose_name='Is Visible')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='url_movie_images', to='movies.movie')),
                ('star', models.ManyToManyField(related_name='url_star_images', to='adminHome.star')),
            ],
        ),
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_top', models.BooleanField(default=False, verbose_name='Is Top Star')),
                ('character_name', models.CharField(max_length=100)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminHome.star')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='rate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.movierate'),
        ),
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(blank=True, to='movies.movietag'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.ManyToManyField(blank=True, null=True, related_name='writer_movies', to='adminHome.star'),
        ),
        migrations.CreateModel(
            name='LocalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', validators=[movies.models.validate_not_gif], verbose_name='Image File')),
                ('is_main', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_movie_images', to='movies.movie')),
                ('star', models.ManyToManyField(related_name='local_star_images', to='adminHome.star')),
            ],
        ),
    ]
