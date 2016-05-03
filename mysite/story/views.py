from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from story.models import Story, Chapter
from author.models import Author
from response.models import Response


@login_required
def create_story(request, author_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        story = Story(author=author)
        story.story_title = title
        story.story_description = description
        if image:
            story.story_image = image

        story.save()
        return redirect('author:show_profile', author)
    return render(request, "story/add_story.html")


@login_required
def edit_story(request, author_slug=None, story_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    story = get_object_or_404(Story, story_slug=story_slug)

    if request.user != author.user:
        return redirect('author:show_profile', request.user)

    context = {
        "author": author,
        "story": story,
    }

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if image:
            story.story_image = image

        story.story_title = title
        story.story_description = description

        story.save()
        return redirect('author:show_profile', author)
    return render(request, "story/edit_story.html", context)


def story(request, author_slug=None, story_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    story = get_object_or_404(Story, story_slug=story_slug)
    chapter_list = Chapter.objects.filter(story=story).order_by("chapter_number")
    responses = Response.objects.filter(chapter__story=story).order_by("-posted")
    today = timezone.now()
    context = {
        "author": author,
        "story": story,
        "chapter_list": chapter_list,
        "responses": responses,
        "today": today,
    }
    return render(request, "story/story.html", context)


def home(request):
    story_list = Story.objects.all().order_by("-time_updated")
    query = request.GET.get("q")
    if query:
        story_list = story_list.filter(
            Q(story_title__icontains=query) |
            Q(author__user__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(chapter__chapter_title__icontains=query)
        ).distinct()
    paginator = Paginator(story_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        story = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        story = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        story = paginator.page(paginator.num_pages)
    context = {
        "stories": story,
        "page_request_var": page_request_var,

    }
    return render(request, "story/home.html", context)


def top_stories(request):
    return render(request, "story/top_stories.html")


@login_required
def create_chapter(request, author_slug=None, story_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    story = get_object_or_404(Story, story_slug=story_slug)

    if request.user != author.user:
        return redirect('author:show_profile', request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        number = request.POST.get('number')
        content = request.POST.get('content')

        chapter = Chapter(story=story)
        chapter.chapter_title = title
        chapter.chapter_number = number
        chapter.chapter_content = content
        chapter.save()

        return redirect('author:show_profile', author)
    return render(request, "story/add_chapter.html")


@login_required
def edit_chapter(request, author_slug=None, story_slug=None, chapter_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    story = get_object_or_404(Story, story_slug=story_slug)
    chapter = get_object_or_404(Chapter, chapter_slug=chapter_slug)

    if request.user != author.user:
        return redirect('author:show_profile', request.user)

    context = {
        "author": author,
        "story": story,
        "chapter": chapter,
    }
    if request.method == "POST":
        title = request.POST.get('title')
        number = request.POST.get('number')
        content = request.POST.get('content')

        chapter.chapter_title = title
        chapter.chapter_number = number
        chapter.chapter_content = content
        chapter.save()
    return render(request, "story/edit_chapter.html", context)


def chapter(request, author_slug=None, story_slug=None, chapter_slug=None):
    author = get_object_or_404(Author, author_slug=author_slug)
    story = get_object_or_404(Story, story_slug=story_slug)
    chapter = get_object_or_404(Chapter, chapter_slug=chapter_slug)
    chapter_list = Chapter.objects.filter(story=story).order_by("chapter_number")
    comments = Response.objects.filter(chapter=chapter).order_by("-posted")
    today = timezone.now()
    context = {
        "author": author,
        "story": story,
        "chapter": chapter,
        "chapter_list": chapter_list,
        "comments": comments,
        "today": today,
    }
    if request.method == "POST":
        if not (request.user.is_authenticated and request.user.is_active):
            return redirect('main:sign_in')

        content = request.POST.get('content')
        like = request.POST.get('like', False)

        response = Response(chapter=chapter)
        response.commenter = request.user
        response.content = content
        response.like = like
        response.save();

        return redirect('story:chapter', author.user.username, story.story_slug, chapter.chapter_slug)

    return render(request, "story/chapter.html", context)
