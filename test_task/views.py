from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from models import Product, Comment, Likes
from forms import CommentForm
from django.contrib import messages
from django.utils import timezone as t
from django.db.models import Count
from django.core.cache import cache


class ProductList(View):

    def get(self, request):
        if 'products' not in cache:
            products = Product.objects.annotate(
                action_count=Count('product_like')).order_by(
                request.GET.get('order_by', '-action_count')).values(
                'name', 'slug', 'description', 'price', 'action_count')
            cache.set('products', products, 60)
        else:
            products = cache.get('products')

        context = {'products': products}
        return render(request, 'test_task/product_list.html',
                      context)


class ProductDetail(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        like = True
        if request.user.is_authenticated():
            like = Likes.objects.filter(user=request.user,
                                        product=product).exists()
        comments = Comment.objects.filter(product=product,
                                          pub_date__range=[
                                              t.now() - t.timedelta(hours=24),
                                              t.now()
                                          ]).values('name', 'comment')
        form = CommentForm(initial={'product': product})

        context = {'product': product,
                   'comments': comments,
                   'form': form,
                   'like': like}
        return render(request, 'test_task/product_detail.html',
                      context)

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        like = True
        if request.user.is_authenticated():
            like = Likes.objects.filter(user=request.user,
                                        product=product).exists()
        comments = Comment.objects.filter(product=product,
                                          pub_date__range=[
                                              t.now() - t.timedelta(hours=24),
                                              t.now()
                                          ]).values('name', 'comment')
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your comment has been added!')
            return redirect(reverse('test_task:product_detail',
                                    args=[product.slug]))
        else:
            messages.error(request, 'Your comment is not added.')

        context = {'product': product,
                   'comments': comments,
                   'form': form,
                   'like': like}
        return render(request, 'test_task/product_detail.html',
                      context)


class AddLike(View):

    def get(self, request, product_id):
        like, created = Likes.objects.get_or_create(
            user=request.user, product_id=product_id)
        if created:
            like.save()
            messages.success(request,
                             'Your like is added!')
        return redirect(request.META.get('HTTP_REFERER'))
