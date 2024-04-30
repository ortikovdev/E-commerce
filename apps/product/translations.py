from modeltranslation.translator import translator, TranslationOptions

from .models import (
    Product,
    Category,
    Tag
)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Category, CategoryTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(Product, ProductTranslationOptions)
