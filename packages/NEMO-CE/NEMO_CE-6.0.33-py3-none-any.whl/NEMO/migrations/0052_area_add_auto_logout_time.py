# Generated by Django 3.2.20 on 2023-08-22 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0051_request_reviewers_in_tool_and_area"),
    ]

    operations = [
        migrations.AddField(
            model_name="area",
            name="auto_logout_time",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Number of minutes after which users will be automatically logged out of this area.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="closure",
            name="staff_absent",
            field=models.BooleanField(
                default=True,
                help_text="Check this box and all staff members will be marked absent during this closure in staff status.",
                verbose_name="Staff absent entire day",
            ),
        ),
    ]
