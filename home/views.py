from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Show, User

# Create your views here.

class IndexView(TemplateView):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):

		context = {
			'bandmembers': [
				{
					'name': 'Mark',
					'instrument': 'Guitarist and Lead Vocalist',
					'bio': 'Loves long walks on the beach',
					'years': 'Member since 1988',
					'photo': 'bandmember.jpg'
				},
				{
					'name': 'Jake',
					'instrument': 'Drummer',
					'bio': "Loves drummin'",
					'years': 'Member since 1988',
					'photo': 'bandmember.jpg'
				},
				{
					'name': 'Kyle',
					'instrument': 'Bass',
					'bio': "Enjoys farting and smokin' rocks",
					'years': 'Member since 2005',
					'photo': 'bandmember.jpg'
				}
			]
		}

		return render(request, self.template_name, context)


class ContactView(TemplateView):
	template_name = "contact.html"

class LiveShowsView(TemplateView):
	template_name = "shows.html"

	def get(self, request, *args, **kwargs):
		context = {'shows': Show.objects.all()}
		return render(request, self.template_name, context)

def add_user_to_mailing_list(request):
	status_code = 400 #set to 400 once view is complete
	data,created = {},False

	if not request.POST or not request.is_ajax():
		status_code = 405

	email = request.POST.get("email")

	if email:
		user,created = User.objects.update_or_create(email=email, defaults={"email":email, "notify":True})
		status_code = 200


	data.update({"email": email, "created": created})
	response = JsonResponse(data, content_type="application/json")
	response.status_code = status_code

	return response
