from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Author
from story.models import Story, Chapter


@login_required
def show_profile(request, author_slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Author, author_slug=author_slug)
    story_list = Story.objects.filter(author=instance)
    context = {
        "instance": instance,
        "story_list": story_list,
    }
    return render(request, "author/profile.html", context)


@login_required
def update_profile(request, author_slug=None):
    instance = get_object_or_404(Author, author_slug=author_slug)

    if request.user != instance.user:
        raise Http404
    if request.method == "POST":
        instance.first_name = request.POST.get('first_name')
        instance.last_name = request.POST.get('last_name')

        if request.FILES.get('image'):
            instance.author_image = request.FILES.get('image')

        instance.author_bio = request.POST.get('bio')
        instance.save()
        return redirect('story:home')
    context = {
        "instance": instance,
    }
    return render(request, 'author/update_profile.html', context)
