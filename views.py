from django.shortcuts import render

# url does not exist
def custom_404(request):
    return render(request, '404.html', status=404)