# Generated by Django 3.2.8 on 2022-01-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_pdf_file_bloodtest_client_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodtest',
            name='client_ip',
            field=models.CharField(default='unknown ip', max_length=45),
        ),
    ]
