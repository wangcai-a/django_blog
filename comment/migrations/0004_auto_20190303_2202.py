# Generated by Django 2.1.4 on 2019-03-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20190303_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='root_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply_root', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply_parent', to='comment.Comment'),
        ),
    ]
