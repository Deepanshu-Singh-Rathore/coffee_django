from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email using current Django email settings."

    def add_arguments(self, parser):
        parser.add_argument('--to', dest='to', help='Override recipient address')
        parser.add_argument('--subject', dest='subject', default='SMTP test from Django', help='Email subject')
        parser.add_argument('--message', dest='message', default='If you received this, SMTP is configured.', help='Email body')

    def handle(self, *args, **options):
        to_email = options['to'] or getattr(settings, 'CONTACT_EMAIL_TO', None)
        if not to_email:
            self.stderr.write(self.style.ERROR('No recipient found. Set CONTACT_EMAIL_TO or pass --to'))
            return 1
        subject = options['subject']
        message = options['message']
        sent = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
        if sent:
            self.stdout.write(self.style.SUCCESS(f"Sent test email to {to_email}"))
        else:
            self.stderr.write(self.style.ERROR("Email send returned 0"))
        return 0
