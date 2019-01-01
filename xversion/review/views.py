from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from .models import Review, CategoryModel
from review.forms import ReviewForm
import datetime
import json


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'review/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review/review_detail.html', {'review': review})


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
        review.model = model
        review.user_name = user_name
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
    instance = Review.objects.get(id=comment_id, model=model_id)
    instance.delete()
    return HttpResponse(request)


def edit_review(request, model_id, comment_id):
    form = ReviewForm()
    return render(request, 'review/review_edit.html', {'form': form})
