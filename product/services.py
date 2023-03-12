from category.models import Category
from personal_account.models import ViewsHistory
from .models import Product
from .forms import AddReviewForm


class ProductService:

    @staticmethod
    def user_has_review(user, product: Product):
        if user.is_authenticated:
            reviews = product.reviews.all()
            curr_usr_review = reviews.filter(user=user).exists()
            if curr_usr_review:
                return True
        return False

    @staticmethod
    def review_form_save(instance, request):
        if (
            not ProductService.user_has_review(instance.request.user, instance.object)
            and instance.request.user.is_authenticated
        ):
            review_form = AddReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = instance.object
                review.user = request.user
                review.save()

    @staticmethod
    def views_increment(instance):
        product = instance.get_object()
        product.views += 1
        product.save()

    @classmethod
    def get_all_categories(cls):
        categories = Category.objects.all()
        return categories
