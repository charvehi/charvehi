from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from .models import Review, CategoryModel
from review.forms import ReviewForm
import datetime
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.models import User
User = get_user_model()

from booking.views import category_model_list
import json


def review_list(request, model_id):
    comment_added = request.GET.get('comment_added')
    details = CategoryModel.objects.filter(m_id=model_id)
    if comment_added == 'true':
        latest_review_list = Review.objects.filter(model=model_id).order_by('-pub_date')[:3]
    else:
        latest_review_list = Review.objects.filter(model=model_id).order_by('-pub_date')[:9]

    review_exist = Review.objects.filter(user_id=request.user.id)
    review = False
    if review_exist.exists():
        review = True
    context = {
        'latest_review_list': latest_review_list,
        'modeldetails': details,
        'review_bit': review,
    }
    return render(request, 'review/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review_exist = Review.objects.filter(user_id=request.user.id)
    review_bit = False
    print(review.user_id)
    print(request.user)
    if review_exist.exists() and review.user_id == request.user:
        review_bit = True
    print(review_bit)
    return render(request, 'review/review_detail.html', {'review': review, 'review_bit': review_bit})


@require_POST
def add_review(request, model_id):
    model = get_object_or_404(CategoryModel, m_id=model_id)
    if request.is_ajax() and request.method == 'POST':
        #form = ReviewForm(request.POST)
        user_name = request.POST.get('user_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        """
        if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        """
        review = Review()
        user = User.objects.get(id=request.user.id)
        review.model = model
        review.user_id = user
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('booking:category_model_details', args=[model.m_id, model.slug]))
        return HttpResponse(review)
    else:
            print("form invalid")

    return render(request, 'booking/catmodel/model_detail.html', {'model': model, 'form': form})


def del_review(request, model_id, comment_id):
    review = Review.objects.get(id=comment_id, model=model_id)
    review.delete()
    return HttpResponse(request)


def edit_review(request, comment_id):
    commit = request.GET.get('commit')
    db_comment = request.GET.get('comment')

    if request.method == 'POST':
        print("data posted")
        form = ReviewForm(request.POST)
        #if form.is_valid():
        review = Review.objects.get(id=comment_id)
        comment = form.data['comment']
        review.comment = comment
        review.save(update_fields=['comment'])
        if commit == 'true':
            return HttpResponse("Changes made")

    form = ReviewForm()
    context = {
            'form_edit': form,
            'r_id': comment_id,
            'review': db_comment,
        }
    return render(request, 'review/review_edit.html', context)
