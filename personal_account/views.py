from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ProfileEditForm
from order.models import Order
from .models import ViewsHistory


class AccountView(View):
    template_name = "users/account.html"

    def get(self, request):
        last_order = Order.objects.filter(consumer=request.user, order_in=True).first()
        viewshistorys = ViewsHistory.objects.filter(user_id=request.user.id)
        return render(request, self.template_name, context={"last_order": last_order, "viewshistorys": viewshistorys})


class ProfileView(View):
    template_name = "users/profile.html"

    def get(self, request):
        form = ProfileEditForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account")
        return render(request, self.template_name, context={"form": form})
