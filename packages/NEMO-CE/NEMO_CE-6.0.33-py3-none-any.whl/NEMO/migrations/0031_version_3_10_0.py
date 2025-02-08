# Generated by Django 2.2.20 on 2021-04-15 15:45
from django.conf import settings
from django.db import migrations, models

import NEMO.fields
from NEMO.migrations_utils import create_news_for_version


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0030_version_3_9_2"),
    ]

    def new_version_news(apps, schema_editor):
        create_news_for_version(apps, "3.10.0")

    operations = [
        migrations.AddField(
            model_name="project",
            name="only_allow_tools",
            field=models.ManyToManyField(
                blank=True, help_text="Selected tools will be the only ones allowed for this project.", to="NEMO.Tool"
            ),
        ),
        migrations.AddField(
            model_name="toolusagecounter",
            name="warning_email",
            field=NEMO.fields.MultiEmailField(
                blank=True,
                help_text="The address to send the warning email to. A comma-separated list can be used.",
                max_length=2000,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="toolusagecounter",
            name="warning_threshold",
            field=models.FloatField(
                blank=True,
                help_text="When set in combination with the email address, a warning email will be sent when the counter reaches this value.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="toolusagecounter",
            name="warning_threshold_reached",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="project",
            name="allow_consumable_withdrawals",
            field=models.BooleanField(
                default=True, help_text="Uncheck this box if consumable withdrawals are forbidden under this project"
            ),
        ),
        migrations.AlterField(
            model_name="alert",
            name="title",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="tool",
            name="_tool_calendar_color",
            field=models.CharField(
                db_column="tool_calendar_color",
                default="#33ad33",
                help_text="Color for tool reservations in calendar overviews",
                max_length=9,
            ),
        ),
        migrations.AddField(
            model_name="area",
            name="area_calendar_color",
            field=models.CharField(
                default="#88B7CD", help_text="Color for tool reservations in calendar overviews", max_length=9
            ),
        ),
        migrations.AddField(
            model_name="tool",
            name="_superusers",
            field=models.ManyToManyField(
                blank=True,
                db_table="NEMO_tool_superusers",
                help_text="Superusers who can train users on this tool.",
                related_name="superuser_for_tools",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(new_version_news),
    ]
