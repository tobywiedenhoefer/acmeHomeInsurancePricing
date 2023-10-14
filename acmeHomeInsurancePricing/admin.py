from django.contrib import admin
from .models import Quote, QuoteRule, State

admin.site.register(QuoteRule)
admin.site.register(Quote)
admin.site.register(State)
