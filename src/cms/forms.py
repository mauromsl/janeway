__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"


from django import forms
from django.apps import apps
from django.http import Http404

from ajax_select import register, LookupChannel
from ajax_select.fields import AutoCompleteSelectMultipleField
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget

from cms import models
from submission import models as submission_models


class PageForm(forms.ModelForm):

    class Meta:
        model = models.Page
        exclude = ('journal', 'is_markdown', 'content_type', 'object_id')

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget = SummernoteWidget()

class CMSPageForm(forms.ModelForm):

    class Meta:
        model = models.CMSPage
        exclude = ('journal', 'press')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            super(PageForm, self).__init__(*args, **kwargs)

class NavForm(forms.ModelForm):

    class Meta:
        model = models.NavigationItem
        exclude = ('page', 'content_type', 'object_id')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(NavForm, self).__init__(*args, **kwargs)

        self.fields['top_level_nav'].queryset = models.NavigationItem.objects.filter(
            content_type=request.model_content_type,
            object_id=request.site_type.pk,
            has_sub_nav=True,
        )


class CMSBlockForm(forms.ModelForm):
    class Meta:
        exclude = ('page', 'sequence')


class AboutBlockForm(CMSBlockForm):
    class Meta(CMSBlockForm.Meta):
        model = models.AboutBlock


class HTMLBlockForm(CMSBlockForm):
    class Meta(CMSBlockForm.Meta):
        model = models.HTMLBlock


class NewsBlockForm(CMSBlockForm):
    class Meta(CMSBlockForm.Meta):
        model = models.NewsBlock


class FeaturedJournalsBlockForm(CMSBlockForm):
    class Meta(CMSBlockForm.Meta):
        model = models.FeaturedJournalsBlock


class FeaturedArticlesBlockForm(CMSBlockForm):
    featured_articles = AutoCompleteSelectMultipleField('articles')

    class Meta(CMSBlockForm.Meta):
        model = models.FeaturedArticlesBlock

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)
        featured_articles = self.cleaned_data.pop("featured_articles", [])

        if commit == True:
            instance.save()
            for seq, article in enumerate(featured_articles, start=1):
                related, _ = models.CMSFeaturedArticle.objects.get_or_create(
                    article=article,
                    cms_block=instance,
                )
                related.sequence = seq
                related.save()



@register("articles")
class FeaturedArticleLookup(LookupChannel):
    model = submission_models.Article
    def get_query(self, query_term, request):
        articles = self.model.objects.filter(stage="Published")
        if request.journal:
            articles = articles.filter(journal=request.journal)
        search_filter = (
                Q(pk__contains=query_term if query_term.isdigit() else 0)
                | Q(title__icontains=query_term))
        return articles.filter(search_filter)



def prepare_cms_forms(cms_blocks):
    prepared_forms = dict(CMS_BLOCK_FORMS)
    for block in cms_blocks:
        form = prepared_forms.get(block.__class__)
        if form:
            prepared_forms[block.__class__] = form(instance=block)

    return prepared_forms


def save_cms_block(prepared_forms, new_data):
    model = apps.get_model(app_label="cms", model_name=new_data["block"])
    form = prepared_forms.get(model)
    if model not in prepared_forms:
        raise Http404()

    # TODO: There must be a way of updating the form without reinstantiating...
    form = form.__class__(new_data, instance=form.instance)
    prepared_forms[model] = form
    return form.save()


CMS_BLOCK_FORMS = {
    form.Meta.model: form
    for form in (
        AboutBlockForm,
        HTMLBlockForm,
        NewsBlockForm,
        FeaturedJournalsBlockForm,
        FeaturedArticlesBlockForm,
    )
}
