from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from config.decorators import allowed_users


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

    @login_required(login_url='/auth/login/')
    # @allowed_users(allowed_roles=['admin'])
    def home(request):
        context = {}
        context = TemplateLayout().init(context)

        return render(request, 'dashboard_analytics.html', context)
