from django.core.mail import send_mail

def send_email_on_login(request, ip):
    subject = f"Your Ip address is {ip}"
    message = f"Hello You are login on this ip address {ip}"
    send_mail(subject, message, 'thecode8228@gmail.com',{request.user.email})