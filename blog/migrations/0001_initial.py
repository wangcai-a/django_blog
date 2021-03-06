# Generated by Django 2.1.4 on 2018-12-09 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('readed_num', models.IntegerField(default=0)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
