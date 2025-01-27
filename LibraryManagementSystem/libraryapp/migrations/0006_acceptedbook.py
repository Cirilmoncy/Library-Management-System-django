# Generated by Django 5.0.6 on 2024-06-10 04:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0005_bookrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField()),
                ('accepted_date', models.DateTimeField(auto_now_add=True)),
                ('fine', models.IntegerField(default=0)),
                ('return_date', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.librarybookdetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.studentdetails')),
            ],
        ),
    ]
