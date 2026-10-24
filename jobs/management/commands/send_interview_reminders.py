from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from jobs.models import Interview
from notifications.models import Notification


class Command(BaseCommand):
    help = "Send interview reminders 24 hours before the interview"

    def handle(self, *args, **options):
        now = timezone.localtime()
        reminder_window_end = now + timedelta(hours=24)

        interviews = Interview.objects.filter(
            reminder_sent=False
        ).select_related(
            "application__candidate",
            "application__job",
        )

        for interview in interviews:
            interview_datetime = timezone.make_aware(
                datetime.combine(
                    interview.interview_date,
                    interview.interview_time,
                ),
                timezone.get_current_timezone(),
            )

            if now < interview_datetime <= reminder_window_end:
                candidate = interview.application.candidate
                job = interview.application.job

                # Check whether the same reminder already exists
                duplicate_exists = Notification.objects.filter(
                    user=candidate,
                    title="Interview Reminder 🔔",
                    message=(
                        f"Your interview for {job.title} is scheduled "
                        f"for {interview.interview_date} at "
                        f"{interview.interview_time}. "
                        "Please be prepared!"
                    ),
                    notification_type="interview",
                ).exists()

                if not duplicate_exists:
                    Notification.objects.create(
                        user=candidate,
                        title="Interview Reminder 🔔",
                        message=(
                            f"Your interview for {job.title} is scheduled "
                            f"for {interview.interview_date} at "
                            f"{interview.interview_time}. "
                            "Please be prepared!"
                        ),
                        notification_type="interview",
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Reminder created for Interview #{interview.id}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"Duplicate reminder skipped for Interview #{interview.id}"
                    )

                # Mark as processed either way
                interview.reminder_sent = True
                interview.save(update_fields=["reminder_sent"])

        self.stdout.write("Interview reminder check completed.")