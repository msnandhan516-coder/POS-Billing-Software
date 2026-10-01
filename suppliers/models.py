from django.db import models


class Supplier(models.Model):
    company_name = models.CharField(max_length=200)

    contact_person = models.CharField(max_length=150)

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)

    address = models.TextField(blank=True)

    city = models.CharField(max_length=100, blank=True)

    state = models.CharField(max_length=100, blank=True)

    gst_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name