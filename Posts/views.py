from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView


# After add followers models


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = "posts"
    template_name = 'Posts/post/post_list.html'


from .forms import EmailPostForm


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'Posts/post/share.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm


@login_required
def post_create(request):
    if request.method == 'POST':
        # form is sent
        form = PostForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Post added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())

        else:
            # build form with data provided by the Twitter via GET
            form = PostForm(data=request.GET)

        return render(request,
                      'Posts/post/create.html',
                      {'form': form})
