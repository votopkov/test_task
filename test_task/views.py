from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from models import Product, Comment, Likes
from forms import CommentForm
from django.contrib import messages
from django.utils import timezone as t
from django.db.models import Count
from django.core.cache import cache


def product_list(request):
    if 'products' not in cache:
        products = Product.objects.annotate(
            action_count=Count('product_like')).order_by(
            request.GET.get('order_by', '-action_count'))
        cache.set('products', products, 60)
    else:
        products = cache.get('products')

    context = {'products': products}
    return render(request, 'test_task/product_list.html',
                  context)


def product_detail(request, slug):
    if 'product' not in cache:
        product = get_object_or_404(Product, slug=slug)
        cache.set('product', product, 60)
    else:
        product = cache.get('product')
    like_count = Likes.objects.filter(
        product=product).count()
    like = True
    if request.user.is_authenticated():
        try:
            like = Likes.objects.get(user=request.user,
                                     product=product)
        except Likes.DoesNotExist:
            like = False
    comments = Comment.objects.filter(product=product,
                                      pub_date__range=[
                                          t.now() - t.timedelta(hours=24),
                                          t.now()
                                      ])
    form = CommentForm(initial={'product': product.id})

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your comment has been added!')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Your comment is not added.')

    context = {'product': product,
               'comments': comments,
               'form': form,
               'like': like,
               'like_count': like_count}
    return render(request, 'test_task/product_detail.html',
                  context)


@login_required
def add_like(request, product_id):
    like, created = Likes.objects.get_or_create(
        user=request.user, product_id=product_id)
    if created:
        like.save()
        messages.success(request,
                         'Your like is added!')
    return redirect(request.META.get('HTTP_REFERER'))
