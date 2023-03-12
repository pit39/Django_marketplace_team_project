from .models import Category


def get_categories(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return context
