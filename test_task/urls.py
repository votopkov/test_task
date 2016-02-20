from django.conf.urls import patterns, url
from views import ProductList, AddLike, ProductDetail
from django.contrib.auth.decorators import login_required

urlpatterns = patterns(
    '',
    url(r'^$', ProductList.as_view(), name='product_list'),
    url(r'^product_detail/(?P<slug>[\w-]+)$',
        ProductDetail.as_view(), name='product_detail'),
    url(r'^add_like/(?P<product_id>[0-9]+)/$',
        login_required(AddLike.as_view()), name='add_like'),
)
