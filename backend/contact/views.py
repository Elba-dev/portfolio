import json
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ContactView(View):

    def post(self, request):
        # ── Parse JSON body ───────────────────────────────────
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        name    = (data.get('name')    or '').strip()
        email   = (data.get('email')   or '').strip()
        message = (data.get('message') or '').strip()

        # ── Validate ──────────────────────────────────────────
        errors = {}
        if not name:
            errors['name'] = 'Name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        elif '@' not in email:
            errors['email'] = 'Enter a valid email address.'
        if not message:
            errors['message'] = 'Message is required.'

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # ── Send notification email to you ────────────────────
        try:
            send_mail(
                subject=f'[Portfolio] New message from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.OWNER_EMAIL],
                fail_silently=False,
            )

            # ── Auto-reply to the sender ──────────────────────
            send_mail(
                subject='Thanks for reaching out — Elba Ouma',
                message=(
                    f'Hi {name},\n\n'
                    'Thanks for your message! I\'ve received it and '
                    'will get back to you shortly.\n\n'
                    'Best,\nElba Ouma'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Message sent!'}, status=200)

        except Exception as e:
            print(f'Email error: {e}')
            return JsonResponse(
                {'error': 'Failed to send email. Please try again.'},
                status=500
            )

    def get(self, request):
        return JsonResponse({'error': 'Method not allowed.'}, status=405)


class HealthView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok', 'service': 'Elba Ouma Portfolio API'})
