# Generated by Django 4.2.17 on 2025-01-07 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_newsdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplaySection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('display_status', models.IntegerField(default=0)),
                ('display_order', models.IntegerField(default=1)),
                ('display_created_date', models.DateTimeField(verbose_name='Display created date')),
            ],
        ),
        migrations.AddField(
            model_name='newsdata',
            name='display_section',
            field=models.IntegerField(default=0),
        ),
    ]
