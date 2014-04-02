from django.shortcuts import render

def home(request):
	sample_list = ["one", "two", "three"]
	context = {'var_name': sample_list}
	return render(request, 'tracker/home.html', context)

def explore(request, sort_by):
	if sort_by == "":
		sort_by = "sessions"

	data = {}
	data['sessions'] = ["October 2013", "April 2013", "October 2012", "April 2012"]
	data['topics'] = ["Faith", "Repentance", "Baptism", "Holy Ghost"]
	data['speakers'] = ["President Thomas S. Monson", "President Dieter F. Uchtdorf", "President Henry B. Eyring"]

	context = {'categories': data[sort_by], "sort_by": sort_by[:-1]}
	return render(request, 'tracker/explore.html', context)