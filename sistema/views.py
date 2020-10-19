from django.shortcuts import render

# Create your views here.

def landing_page(request):

	context = {
		"variavel_1": "Hoje é um grande dia",
		"variavel_2": 109,
	}

	return render(request, "landing_page.html", context)