# Generated by Django 5.2.1 on 2025-06-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='caste',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='candidate',
            name='category',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_city',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_district',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_line1',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_line2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_pincode',
            field=models.CharField(default='Unknown', max_length=10),
        ),
        migrations.AddField(
            model_name='candidate',
            name='communication_state',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='email',
            field=models.EmailField(default='unknown@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_city',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_district',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_line1',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_line2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_pincode',
            field=models.CharField(default='Unknown', max_length=10),
        ),
        migrations.AddField(
            model_name='candidate',
            name='permanent_state',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='phone',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='candidate',
            name='religion',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='candidate',
            name='same_as_permanent',
            field=models.BooleanField(default=False),
        ),
    ]
