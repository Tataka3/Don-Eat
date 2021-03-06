# Generated by Django 2.2.4 on 2022-04-09 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.FloatField()),
                ('category', models.CharField(choices=[('VEG', 'VEG'), ('NON VEG', 'NON VEG')], default='VEG', max_length=100, null=True)),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('freshTill', models.IntegerField(default=0)),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.ProfileModel')),
            ],
        ),
    ]
