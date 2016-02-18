from django.conf.urls import patterns, url


urlpatterns = patterns(
    'test_task.views',
    url(r'^$', 'product_list', name='product_list'),
    url(r'^product_detail/(?P<slug>[\w-]+)$',
        'product_detail', name='product_detail'),
    url(r'^add_like/(?P<product_id>[0-9]+)/$', 'add_like', name='add_like'),
)
