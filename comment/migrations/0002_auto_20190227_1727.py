# Generated by Django 2.1.4 on 2019-02-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='comment',
            name='root_id',
            field=models.IntegerField(default=0),
        ),
    ]
