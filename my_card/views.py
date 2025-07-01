# views.py
from django.shortcuts import render, redirect
from .models import UserCard
from .forms import UserCardAdminForm
from django.contrib.auth.decorators import login_required

def create_card(request):
    if not request.user.is_staff:
        return redirect('my_card')  # Or return 403

    form = UserCardAdminForm()

    if request.method == 'POST':
        form = UserCardAdminForm(request.POST, request.FILES)
        if form.is_valid():
            selected_user = form.cleaned_data['user']
            if UserCard.objects.filter(user=selected_user).count() < 10:
                form.save()
                return redirect('my_card')  # or redirect to a user-specific view
            else:
                form.add_error(None, f"{selected_user.username} has already uploaded 10 cards.")

    return render(request, 'create_card.html', {'form': form})
@login_required
def my_card(request):
    cards = UserCard.objects.filter(user=request.user)
    return render(request, 'my_card.html', {'cards': cards})
