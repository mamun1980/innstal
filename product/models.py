# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re
from django.db import models
from usms.models import *
# Create your models here.

# class Company(models.Model):
#     name = models.CharField(max_length=100, db_index=True)
#     company_phone = models.CharField(_('Company Phone Number'), max_length=15, blank=True, null=True)
#     address = models.TextField(max_length=200, blank=True, null=True)
#
#     def __unicode__(self):
#         return self.name

def category_directory_path(instance, filename):
    name = instance.name

    filepath = 'product/category/'

    filepath = filepath + name + filename[-4:]

    return filepath

class ProductCategory(models.Model):
    name = models.CharField(_('Product Category'), max_length=50, db_index=True)
    category_image = ProcessedImageField(upload_to=category_directory_path,
        processors=[ResizeToFill(200, 150)], format='JPEG', options={'quality': 80}, blank=True, null=True)

    def __unicode__(self):
        return self.name

class ProductType(models.Model):
    type_name = models.CharField(_('Type Name'), max_length=50, db_index=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True)

    def __unicode__(self):
        return self.type_name

# class ProductModel(models.Model):
#     model_no = models.CharField(_('Model No'), max_length=50, db_index=True)
#     Company = models.ForeignKey(Company, blank=True, null=True)
#
#     def __unicode__(self):
#         return self.model_no

class ProductBrand(models.Model):
    brand_name = models.CharField(_('Brand Name'), max_length=50, db_index=True)

    def __unicode__(self):
        return self.brand_name

def product_image_path(instance, filename):
    # import pdb; pdb.set_trace()
    filepath = 'product/'
    name = re.sub(" ","-",instance.product_name)
    model = re.sub(" ","-", instance.product_model)
    if instance.product_brand:
        brand = re.sub(" ","-", instance.product_brand.brand_name)
        filepath = filepath + brand + '/'

    if model:
        filepath = filepath + model + '/'

    filepath = filepath + name + '/images/' + name + filename[-4:]

    return filepath

def product_manual_path(instance, filename):
    # import pdb; pdb.set_trace()
    filepath = 'product/'
    name = re.sub(" ","-",instance.product_name)
    model = re.sub(" ","-", instance.product_model)

    if instance.product_brand:
        brand = re.sub(" ","-", instance.product_brand.brand_name)
        filepath = filepath + brand + '/'

    if model:
        filepath = filepath + model + '/'

    filepath = filepath + name + '/manual/' + name+filename[-4:]

    return filepath


class Product(models.Model):
    product_name = models.CharField(_('Product Name'), max_length=50, db_index=True)
    business = models.ForeignKey(InnstalUser, blank=True, null=True)
    product_category = models.ForeignKey(ProductCategory, blank=True, null=True)
    product_type = models.ForeignKey(ProductType, blank=True, null=True)
    product_brand = models.ForeignKey(ProductBrand, blank=True, null=True)
    product_model = models.CharField(_('Model No'), max_length=50, blank=True, null=True)
    warranty_duration = models.CharField(_('Warranty In Days'), max_length=5, blank=True, null=True)
    installation_instruction = models.TextField(max_length=500, blank=True, null=True)
    product_image1 = ProcessedImageField(upload_to=product_image_path,
        processors=[ResizeToFill(200, 150)], format='JPEG', options={'quality': 80}, blank=True, null=True)
    product_manual = models.FileField(upload_to=product_manual_path, blank=True, null=True)
    product_search_string = models.TextField(max_length=500, blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.product_name

    def save(self, *args, **kwargs):

        string = self.product_name + " "
        if self.product_model:
            string += self.product_model + " "

        if self.product_brand:
            string += self.product_brand.brand_name + " "

        if self.product_category:
            string += self.product_category.name + " "
        self.product_search_string = string
        super(Product, self).save(*args, **kwargs)


class ProductReview(models.Model):
    product = models.ForeignKey(Product)
    writer = models.ForeignKey(InnstalUser)
    review = models.TextField(max_length=250)
    review_date = models.DateTimeField(auto_now_add=True, editable=False)


class ProductVisited(models.Model):
    product = models.ForeignKey(Product)
    visitor = models.ForeignKey(InnstalUser)
    visite_date = models.DateTimeField(auto_now_add=True, editable=False)
