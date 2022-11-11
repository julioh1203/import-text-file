from django.conf import settings


def handle_uploaded_file(file_name):
    with open(f'{settings.MEDIA_ROOT}/{file_name}', 'wb+') as destination:
        for chunk in file_name.chunks():
            destination.write(chunk)