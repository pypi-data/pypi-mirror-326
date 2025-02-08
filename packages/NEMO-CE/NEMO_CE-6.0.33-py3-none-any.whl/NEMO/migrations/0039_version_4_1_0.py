# Generated by Django 3.2.12 on 2022-04-07 14:17

from django.db import migrations, models

from NEMO.migrations_utils import create_news_for_version


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0038_version_4_0_0"),
    ]

    def new_version_news(apps, schema_editor):
        create_news_for_version(apps, "4.1.0", "")

    operations = [
        migrations.RunPython(new_version_news),
        migrations.AddField(
            model_name="landingpagechoice",
            name="hide_from_staff",
            field=models.BooleanField(
                default=False,
                help_text="Hides this choice from staff and technicians. When checked, only normal users, facility managers and super-users can see the choice",
            ),
        ),
        migrations.AlterField(
            model_name="landingpagechoice",
            name="hide_from_users",
            field=models.BooleanField(
                default=False,
                help_text="Hides this choice from normal users. When checked, only staff, technicians, facility managers and super-users can see the choice",
            ),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_alternate",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_access_request_updates",
            field=models.BooleanField(default=True, help_text="Send access request updates to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_buddy_request_replies",
            field=models.BooleanField(default=True, help_text="Send buddy request replies to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_reservation_emails",
            field=models.BooleanField(default=True, help_text="Send reservation emails to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_reservation_ending_reminders",
            field=models.BooleanField(
                default=True, help_text="Send reservation ending reminders to my alternate email"
            ),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_reservation_reminders",
            field=models.BooleanField(default=True, help_text="Send reservation reminders to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_task_updates",
            field=models.BooleanField(default=True, help_text="Send task updates to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_usage_reminders",
            field=models.BooleanField(default=True, help_text="Send usage reminders to my alternate email"),
        ),
        migrations.AddField(
            model_name="userpreferences",
            name="email_send_broadcast_emails",
            field=models.BooleanField(default=True, help_text="Send broadcast emails to my alternate email"),
        ),
        migrations.AlterField(
            model_name="emaillog",
            name="category",
            field=models.IntegerField(
                choices=[
                    (0, "General"),
                    (1, "System"),
                    (2, "Direct Contact"),
                    (3, "Broadcast Email"),
                    (4, "Timed Services"),
                    (5, "Feedback"),
                    (6, "Abuse"),
                    (7, "Safety"),
                    (8, "Tasks"),
                    (9, "Access Requests"),
                    (10, "Sensors"),
                ],
                default=0,
            ),
        ),
    ]
