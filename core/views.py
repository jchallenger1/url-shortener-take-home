from django.shortcuts import render
from django.views import View
from django.views.generic.base import RedirectView

from core.models import Url
from core.forms import UrlForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("url")
        obj = Url.objects.create(url=url)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url()}
        )

class HashUrlRedirectView(RedirectView):
    # Redirects a hashedurl to the original url
    # Responses as the original url or 410 if not found
    # https://docs.djangoproject.com/en/4.2/ref/class-based-views/base/#redirectview
    permanent = False
    query_string = False
    pattern_name = ""
    
    def get_redirect_url(self, *args, **kwargs):
        
        if "hashed_url" in kwargs:
            matched_urls = Url.objects.filter(hashed_url=kwargs["hashed_url"])
            if (len(matched_urls) == 1):
                self.url = matched_urls[0].url
        else:
            # Note: Normally this would be put into some log file
            print(f"Url [{self.request.get_full_path()}] was redirected but had no hashed_url associated.")
        
        # RedirectView handles the 410 or original url depending on if self.url is set to the url or None
        return super().get_redirect_url(*args, **kwargs)
        