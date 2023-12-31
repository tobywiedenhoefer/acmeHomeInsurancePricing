from django.contrib import admin
from django.urls import path
from acmeHomeInsurancePricing import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quotes/<int:quote_id>", views.get_quote, name="get_quote"),
    path("quotes/submit", views.submit_quote, name="submit_quote"),
]
