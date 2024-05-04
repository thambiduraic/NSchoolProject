# Generated by Django 4.2.11 on 2024-05-02 12:08

import Admin_Login_App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_Login_App', '0003_alter_courses_description_alter_courses_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='partners_logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to=Admin_Login_App.models.getlogo)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('modified_by', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
