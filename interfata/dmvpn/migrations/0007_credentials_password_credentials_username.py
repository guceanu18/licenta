# Generated by Django 4.1.7 on 2023-03-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dmvpn", "0006_credentials_delete_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="credentials",
            name="password",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="credentials",
            name="username",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
