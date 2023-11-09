from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import User
from myapp.forms import UserForm
from django.shortcuts import get_object_or_404

# Update user
@login_required(login_url='login')
def updateUser(request, pk):
    """
    View function to update a user's information.

    Args:
        request: The HTTP request object.
        pk: The primary key of the user to be updated.

    Returns:
        A redirection to the update user page after successfully updating the user,
        or a rendered HTML template for the update user page if it's a GET request.
    """
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('update-user', pk=user.id)
    else:
        form = UserForm(instance=user, user=request.user)

    context = {'form':form, 'page':'update'}

    return render(request, "authenticate/user_update.html", context)
