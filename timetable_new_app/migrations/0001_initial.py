# Generated by Django 2.0.2 on 2019-03-21 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fac_id', models.IntegerField(null=True)),
                ('faculty_name', models.CharField(max_length=10)),
                ('theory_hours', models.IntegerField()),
                ('practical_hours', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=15)),
                ('slot', models.CharField(max_length=5)),
                ('availability', models.IntegerField()),
                ('faculty_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_Subject_Totalhours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_hours', models.IntegerField()),
                ('faculty_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='LabAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
                ('slot', models.CharField(max_length=5)),
                ('batch', models.CharField(max_length=5)),
                ('lab_no', models.CharField(max_length=5)),
                ('sem', models.IntegerField()),
                ('division', models.CharField(max_length=2)),
                ('faculty_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='LoadAllocate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=10, null=True)),
                ('theory_hours', models.IntegerField()),
                ('pract_hours', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sem_4_C',
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
            name='Sem_4_C_lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch1', models.CharField(max_length=500)),
                ('batch2', models.CharField(max_length=500)),
                ('batch3', models.CharField(max_length=500)),
                ('batch4', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Sem_4_D',
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
            name='Sem_4_D_lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch1', models.CharField(max_length=500)),
                ('batch2', models.CharField(max_length=500)),
                ('batch3', models.CharField(max_length=500)),
                ('batch4', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Sem_6_C',
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
            name='Sem_6_C_lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch1', models.CharField(max_length=500)),
                ('batch2', models.CharField(max_length=500)),
                ('batch3', models.CharField(max_length=500)),
                ('batch4', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Sem_6_D',
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
            name='Sem_6_D_lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch1', models.CharField(max_length=500)),
                ('batch2', models.CharField(max_length=500)),
                ('batch3', models.CharField(max_length=500)),
                ('batch4', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('sub_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('theory_hours', models.IntegerField()),
                ('practical_hours', models.IntegerField()),
                ('allocated', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TheoryAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=15)),
                ('faculty_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Faculty')),
                ('sub_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Subject')),
            ],
        ),
        migrations.AddField(
            model_name='laballocation',
            name='sub_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Subject'),
        ),
        migrations.AddField(
            model_name='faculty_subject_totalhours',
            name='sub_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Subject'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='sub_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_new_app.Subject'),
        ),
    ]
