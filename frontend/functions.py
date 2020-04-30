def handle_uploaded_file(f, directory):
    with open('{directory}/{file_name}'.format(directory=directory, file_name=f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
