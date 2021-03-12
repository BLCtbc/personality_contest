from django.shortcuts import render
from django.views.generic import TemplateView
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
