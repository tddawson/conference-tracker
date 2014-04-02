from django.shortcuts import render

def home(request):
	sample_list = ["one", "two", "three"]
	context = {'var_name': sample_list}
	return render(request, 'tracker/home.html', context)