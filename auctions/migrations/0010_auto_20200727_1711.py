# Generated by Django 3.0.8 on 2020-07-27 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200726_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_comments', to='auctions.Listing'),
        ),
    ]