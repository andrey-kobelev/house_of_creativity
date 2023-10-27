from django.core.paginator import Paginator
from blogicum import settings


def get_page_obj(query_set, request):
    paginator = Paginator(query_set, settings.PAGINATE_BY)
    return paginator.get_page(request.GET.get('page'))
