from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0004_job_reminder_sent"),
    ]

    operations = [
        migrations.AddField(
            model_name="interview",
            name="reminder_sent",
            field=models.BooleanField(default=False),
        ),
    ]