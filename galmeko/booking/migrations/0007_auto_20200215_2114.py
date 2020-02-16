# Generated by Django 3.0.2 on 2020-02-15 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_features'),
        ('booking', '0006_auto_20200215_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingfeature',
            name='feature',
        ),
        migrations.AddField(
            model_name='bookingfeature',
            name='feature',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='setting.Features'),
            preserve_default=False,
        ),
    ]
