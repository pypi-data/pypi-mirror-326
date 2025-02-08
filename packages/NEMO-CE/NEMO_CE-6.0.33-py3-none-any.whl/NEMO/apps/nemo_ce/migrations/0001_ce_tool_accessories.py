# Generated by Django 3.2.18 on 2023-04-25 20:02

from django.db import migrations, models

from NEMO.apps.nemo_ce.migration_utils import NEMOMigration


class Migration(NEMOMigration):

    dependencies = [
        ("NEMO", "0045_version_4_5_0"),
    ]

    operations = [
        migrations.CreateModel(
            name="ToolAccessory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The name of this tool accessory", max_length=200, unique=True)),
                (
                    "tools",
                    models.ManyToManyField(
                        blank=False, help_text="The tools that this accessory can be used with", to="NEMO.Tool"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Tool accessories",
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="reservation",
            name="tool_accessories",
            field=models.ManyToManyField(blank=True, to="NEMO.ToolAccessory"),
        ),
    ]
