# Generated by Django 4.2.11 on 2024-06-04 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NEMO", "0084_remove_tool__allow_delayed_logoff_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactinformation",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="contactinformation",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="contactinformation",
            name="office_location",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
