# Generated by Django 4.1.7 on 2023-03-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dmvpn", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="password",
        ),
        migrations.AddField(
            model_name="user",
            name="password_hash",
            field=models.CharField(default="NULL", max_length=100),
        ),
    ]
