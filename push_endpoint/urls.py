from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from push_endpoint import views

from rest_framework.routers import DefaultRouter, SimpleRouter, Route

urlpatterns = [
    url(r'^pushed_data/$', views.DataList.as_view()),
    url(r'^pushed_data/(?P<pk>[0-9]+)/$', views.DataDetail.as_view(), name='data-detail'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail')
]


class BulkUpdateRouter(DefaultRouter):
    routes = SimpleRouter.routes
    routes[0] = Route(
        url=r'^pushed_data/$',
        mapping={
            'get': 'list',
            'post': 'create',
            'put': 'bulk_update',
            'patch': 'partial_bulk_update'
        },
        name='pushed-data',
        initkwargs={'suffix': 'List'}
    )

router = BulkUpdateRouter()
router.register(r'pushed_data/', views.DataList.as_view(), base_name='pushed-data')

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
