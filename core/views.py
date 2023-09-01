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
        hashed_url = form.cleaned_data.get("hashed_url")
        pin = form.cleaned_data.get("pin")
        shortened_url = form.cleaned_data.get("shortened_url")
        
        if request.POST.get("modify"):
            # hashed_url only contains the hash
            obj_query_set = Url.objects.filter(hashed_url=shortened_url.split('/')[-1], pin=pin)
            
            if not obj_query_set.exists() or not pin:
                return render(request, self.template_name, {"form": form,
                                                            "messages": ["The url and pin combination does not exist."]})
            obj = obj_query_set.first()
            obj.update(hashed_url=hashed_url, url=url)
        else:
            obj = Url.objects.create(url=url, hashed_url=hashed_url, pin=pin)

        return render(request, self.template_name, {"short_url": obj.get_full_short_url()})
        

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
            if matched_urls.exists():
                self.url = matched_urls.first().url
        else:
            # Note: Normally this would be put into some log file
            print(f"Url [{self.request.get_full_path()}] was redirected but had no hashed_url associated.")
        
        # RedirectView handles the 410 or original url depending on if self.url is set to the url or None
        return super().get_redirect_url(*args, **kwargs)
        