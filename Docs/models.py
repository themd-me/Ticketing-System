from django.db import models

# Create your models here.

class Category(models.Model):
    Uzbek_category = models.CharField(max_length=100, blank=True, null=True)
    Russian_category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    langs = {
                "uz": 'Uzbek',
                "ru": 'Russian'
            }
        
    locale = 'uz'
    
    def set_locale(self, locale: str):
        self.locale = locale
        return self

    @property
    def category(self):
        return getattr(self, self.langs[self.locale] + '_category')

    def __str__(self):
        return self.Uzbek_category
        
class Subcategory(models.Model):
    linked_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Uzbek_title = models.CharField(max_length=100, blank=True, null=True)
    Russian_title = models.CharField(max_length=100, blank=True, null=True)
    Uzbek_body = models.CharField(blank=True, null=True)
    Russian_body = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    langs = {
            "uz": 'Uzbek',
            "ru": 'Russian'
        }
    
    locale = 'uz'
    
    def set_locale(self, locale: str):
        self.locale = locale
        return self

    @property
    def title(self):
        return getattr(self, self.langs[self.locale] + '_title')
    
    @property
    def body(self):
        return getattr(self, self.langs[self.locale] + '_body')
    
    def __str__(self):
        return f'{self.linked_category} ─> {self.Uzbek_title}'