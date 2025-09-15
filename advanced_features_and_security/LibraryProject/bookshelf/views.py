from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return render(request, 'bookshelf/book_list.html')
