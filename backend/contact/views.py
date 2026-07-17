import json
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import ContactMessage


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

        # ── Save message to database & send email ─────────────
        try:
            ContactMessage.objects.create(name=name, email=email, message=message)

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
        action = request.GET.get('action')
        if action == 'forgot':
            try:
                send_mail(
                    subject='[Portfolio] Dashboard Access Key Recovery',
                    message=(
                        'Hello,\n\n'
                        'A request was made to retrieve your portfolio admin dashboard access key.\n\n'
                        f'Your access key is: {settings.ADMIN_DASHBOARD_KEY}\n\n'
                        'Please use this key to log in to your custom inbox dashboard at /dashboard.html.\n\n'
                        'Best regards,\nPortfolio System'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.OWNER_EMAIL],
                    fail_silently=False,
                )
                return JsonResponse({'success': True, 'message': 'Key retrieval email sent.'}, status=200)
            except Exception as mail_err:
                print(f"Failed to send key recovery email: {mail_err}")
                return JsonResponse({'error': 'Failed to send retrieval email. Try again later.'}, status=500)

        key = request.GET.get('key')
        if key != settings.ADMIN_DASHBOARD_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        messages = ContactMessage.objects.all().order_by('-created_at')
        data = [
            {
                'id': msg.id,
                'name': msg.name,
                'email': msg.email,
                'message': msg.message,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for msg in messages
        ]
        return JsonResponse({'success': True, 'messages': data}, status=200)

    def delete(self, request):
        key = request.GET.get('key')
        if key != settings.ADMIN_DASHBOARD_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        msg_id = request.GET.get('id')
        if not msg_id:
            return JsonResponse({'error': 'Message ID is required.'}, status=400)
            
        try:
            ContactMessage.objects.get(id=msg_id).delete()
            return JsonResponse({'success': True, 'message': 'Message deleted.'}, status=200)
        except ContactMessage.DoesNotExist:
            return JsonResponse({'error': 'Message not found.'}, status=404)




class HealthView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok', 'service': 'Elba Ouma Portfolio API'})
