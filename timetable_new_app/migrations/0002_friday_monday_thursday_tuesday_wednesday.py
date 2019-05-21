# Generated by Django 2.0.2 on 2019-04-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_new_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1', models.CharField(max_length=100)),
                ('slot2', models.CharField(max_length=100)),
                ('slot3', models.CharField(max_length=100)),
                ('slot4', models.CharField(max_length=100)),
                ('slot5', models.CharField(max_length=100)),
                ('slot6', models.CharField(max_length=100)),
                ('slot7', models.CharField(max_length=100)),
                ('slot8', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Monday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1', models.CharField(max_length=100)),
                ('slot2', models.CharField(max_length=100)),
                ('slot3', models.CharField(max_length=100)),
                ('slot4', models.CharField(max_length=100)),
                ('slot5', models.CharField(max_length=100)),
                ('slot6', models.CharField(max_length=100)),
                ('slot7', models.CharField(max_length=100)),
                ('slot8', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Thursday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1', models.CharField(max_length=100)),
                ('slot2', models.CharField(max_length=100)),
                ('slot3', models.CharField(max_length=100)),
                ('slot4', models.CharField(max_length=100)),
                ('slot5', models.CharField(max_length=100)),
                ('slot6', models.CharField(max_length=100)),
                ('slot7', models.CharField(max_length=100)),
                ('slot8', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tuesday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1', models.CharField(max_length=100)),
                ('slot2', models.CharField(max_length=100)),
                ('slot3', models.CharField(max_length=100)),
                ('slot4', models.CharField(max_length=100)),
                ('slot5', models.CharField(max_length=100)),
                ('slot6', models.CharField(max_length=100)),
                ('slot7', models.CharField(max_length=100)),
                ('slot8', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Wednesday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1', models.CharField(max_length=100)),
                ('slot2', models.CharField(max_length=100)),
                ('slot3', models.CharField(max_length=100)),
                ('slot4', models.CharField(max_length=100)),
                ('slot5', models.CharField(max_length=100)),
                ('slot6', models.CharField(max_length=100)),
                ('slot7', models.CharField(max_length=100)),
                ('slot8', models.CharField(max_length=100)),
            ],
        ),
    ]
