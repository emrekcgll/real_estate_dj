from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def paginator(request, data, view, template_name):
    paginator = Paginator(data, view)
    page = request.GET.get("page")
    try:
        data = paginator.page(page)
        page_range = paginator.page_range[max(0, data.number - 5): data.number + 5]
    except PageNotAnInteger:
        data = paginator.page(1)
        page_range = paginator.page_range[:5]
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        page_range = paginator.page_range[-5:]

    total_items = paginator.count
    items_per_page = len(data)

    context = {
        'data': data,
        'total_items': total_items,
        'items_per_page': items_per_page,
        'page_range': page_range,
    }

    return render(request, template_name, context)