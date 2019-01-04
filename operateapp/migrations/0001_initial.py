# Generated by Django 2.0.6 on 2018-12-02 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('salary', models.IntegerField()),
                ('age', models.SmallIntegerField()),
            ],
            options={
                'db_table': 't_employee',
            },
        ),
    ]
