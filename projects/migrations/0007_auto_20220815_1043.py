# Generated by Django 3.2.12 on 2022-08-15 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20220802_0907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at']},
        ),
    ]
