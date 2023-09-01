import secrets
from django.db import models


class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, blank=True)
    pin = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    # Note: in practice, pin would be hashed instead of directly storing it in the db
    
    def __str__(self):
        return f"{self.pk} - {self.url} - {self.hashed_url}"

    def save(self, *args, **kwargs) -> None:
        # Saves a database object to the database
        self.generate_hashed_url()
        super().save(*args, **kwargs)

    def hash_url(self) -> str:
        # returns a hash url independent from self.url
        token = secrets.token_urlsafe(16)[:10]
        return token

    def get_full_short_url(self) -> str:
        # returns the shortened url
        return f"http://localhost:8000/{self.hashed_url}"
    
    def generate_hashed_url(self) -> None:
        # Generates the hashed_url to self if it is not currently set
        if not self.hashed_url:
            while True:
                # In case of a collision, try to repetively create a new hashed_url
                self.hashed_url = self.hash_url()
                if not Url.objects.filter(hashed_url=self.hashed_url).exists():
                    break
    
    def update(self, hashed_url:str, url:str) -> None:
        # Updates and saves given a hashed_url and url
        self.hashed_url = hashed_url
        self.url = url
        self.save()
        
