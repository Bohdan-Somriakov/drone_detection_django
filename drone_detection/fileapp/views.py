from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os

# File path where the downloadable files are stored
FILE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'files')


def download_file(request, filename):
    file_path = os.path.join('files', filename)

    try:
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except FileNotFoundError:
        return render(request, 'error.html', {'error': 'File not found'})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

def file_list(request):
    # List available files for download
    files = os.listdir(FILE_DIR)
    return render(request, 'fileapp/file_list.html', {'files': files})
