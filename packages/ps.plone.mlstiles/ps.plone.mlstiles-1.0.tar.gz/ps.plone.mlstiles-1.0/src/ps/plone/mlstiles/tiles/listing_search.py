# -*- coding: utf-8 -*-
"""A tile that shows a search form for listings."""

# zope imports
from Acquisition import aq_inner
from Products.CMFPlone import PloneMessageFactory as PMF
from plone.directives import form
from plone.memoize import view
from plone.mls.listing.browser.listing_search import (
    CONFIGURATION_KEY,
    IListingSearch,
    IListingSearchForm,
)
from plone.mls.listing.browser.valuerange.widget import ValueRangeFieldWidget
from z3c.form import button, field
from z3c.form.browser import checkbox, radio
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.traversing.browser.absoluteurl import absoluteURL

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False


class ListingSearchForm(form.Form):
    """Listing Search Form."""

    fields = field.Fields(IListingSearchForm)
    ignoreContext = True
    method = 'get'
    search_url = None

    fields['air_condition'].widgetFactory = radio.RadioFieldWidget
    fields['baths'].widgetFactory = ValueRangeFieldWidget
    fields['lot_size'].widgetFactory = ValueRangeFieldWidget
    fields['interior_area'].widgetFactory = ValueRangeFieldWidget
    fields['beds'].widgetFactory = ValueRangeFieldWidget
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['jacuzzi'].widgetFactory = radio.RadioFieldWidget
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['pool'].widgetFactory = radio.RadioFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget

    def __init__(self, context, request):
        super(ListingSearchForm, self).__init__(context, request)
        form_context = self.getContent()
        if form_context is not None:
            self.prefix = 'form.{0}'.format(form_context.id)

    @property
    def action(self):
        """See interfaces.IInputForm"""
        if self.search_url:
            return self.search_url
        return super(ListingSearchForm, self).action()

    @button.buttonAndHandler(
        PMF(u'label_search', default=u'Search'),
        name='search',
    )
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class ListingSearchTileMixin(object):
    """A tile that shows a search form for listings."""

    @property
    def get_context(self):
        """Return the listing search context."""
        raise NotImplementedError

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(CONFIGURATION_KEY, {})

    def has_listing_search(self, obj):
        """Check if the obj is activated for a listing search."""
        return IListingSearch.providedBy(obj)

    @view.memoize
    def search_url(self):
        """Generate search form url."""
        context = self.get_context
        if not context:
            return ''
        return '/'.join([
            absoluteURL(context, self.request),
            '',
        ])

    @property
    def available_fields(self):
        raise NotImplementedError

    @property
    def search_form(self):
        context = self.get_context
        if not context or not self.has_listing_search(context):
            return

        search_form = ListingSearchForm(aq_inner(context), self.request)
        search_form.fields = search_form.fields.select(*self.available_fields)
        search_form.search_url = self.search_url
        if HAS_WRAPPED_FORM:
            alsoProvides(search_form, IWrappedForm)
        search_form.update()
        return search_form
