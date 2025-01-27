# Generated by Django 5.0.6 on 2024-06-05 13:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarybookdetail',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='StudentSetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=15)),
                ('roll_no', models.IntegerField()),
                ('register_id', models.CharField(max_length=10)),
                ('college_name', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
