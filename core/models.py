import secrets

from django.db import models


class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"{self.pk} - {self.url} - {self.hashed_url}"

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            while True:
                # In case of a collision, try to repetively create a new hashed_url
                self.hashed_url = self.hash_url()
                if not Url.objects.filter(hashed_url=self.hashed_url).exists():
                    break

        super().save(*args, **kwargs)

    def hash_url(self):
        token = secrets.token_urlsafe(16)[:10]
        return token

    def get_full_short_url(self):
        return f"http://localhost:8000/{self.hashed_url}"
