# Generated by Django 3.0.8 on 2020-07-24 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200724_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='This_User_Watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
