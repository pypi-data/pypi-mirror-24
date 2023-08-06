from __future__ import unicode_literals, absolute_import

import json
from collections import OrderedDict
import copy
from datetime import datetime
from decimal import Decimal
from itertools import chain, groupby
import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.db.models import IntegerField, FloatField, TextField, BooleanField, AutoField, CharField, CommaSeparatedIntegerField, DateField, DateTimeField, DecimalField, EmailField, URLField, TimeField, ForeignKey, OneToOneField, ManyToManyField, FileField, ManyToOneRel, ManyToManyRel
from django.db.models.fields import FieldDoesNotExist
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from tri.declarative import should_show, creation_ordered, declarative, getattr_path, sort_after, with_meta, setdefaults_path, dispatch, setattr_path, assert_kwargs_empty, EMPTY, evaluate_recursive
from tri.struct import Struct
from tri.form.render import render_attrs
import six

try:
    from django.template.loader import get_template_from_string
except ImportError:  # pragma: no cover
    # Django 1.8+
    # noinspection PyUnresolvedReferences
    from django.template import engines

    def get_template_from_string(template_code, origin=None, name=None):
        del origin, name  # the origin and name parameters seems not to be implemented in django 1.8
        return engines['django'].from_string(template_code)


__version__ = '4.10.0'  # pragma: no mutate


def capitalize(s):
    return s[0].upper() + s[1:] if s else s


# This input is added to all forms. It is used to circumvent the fact that unchecked checkboxes are not sent as
# parameters in the request. More specifically, the problem occurs when the checkbox is checked by default,
# as it would not be possible to distinguish between the initial request and a subsequent request where the checkbox
# is unchecked. By adding this input, it is possible to make this distinction as subsequent requests will contain
# (at least) this key-value.
AVOID_EMPTY_FORM = '<input type="hidden" name="-" value="-" />'

FULL_FORM_FROM_REQUEST = 'full_form_from_request'
INITIALS_FROM_GET = 'initials_from_get'


DISPATCH_PATH_SEPARATOR = '__'


def handle_dispatch(request, obj):
    for key, value in request.GET.items():
        if key.startswith(DISPATCH_PATH_SEPARATOR):
            remaining_key = key[2:]
            expected_prefix = obj.endpoint_dispatch_prefix
            if expected_prefix is not None:
                parts = remaining_key.split('__', 1)
                prefix = parts.pop(0)
                if prefix != expected_prefix:
                    return True, None
                remaining_key = parts[0] if parts else None
            data = obj.endpoint_dispatch(key=remaining_key, value=value)
            if data is not None:
                return True, HttpResponse(json.dumps(data), content_type='application/json')
    return False, None


def bool_parse(string_value):
    s = string_value.lower()
    if s in ('1', 'true', 't', 'yes', 'y', 'on'):
        return True
    elif s in ('0', 'false', 'f', 'no', 'n', 'off'):
        return False
    else:
        raise ValueError('%s is not a valid boolean value' % string_value)


def foreign_key_factory(model_field, **kwargs):
    setdefaults_path(
        kwargs,
        choices=model_field.foreign_related_fields[0].model.objects.all(),
    )
    kwargs['model'] = model_field.foreign_related_fields[0].model
    return Field.choice_queryset(model_field=model_field, **kwargs)


def many_to_many_factory_read_from_instance(field, instance):
    return getattr_path(instance, field.attr).all()


def many_to_many_factory(model_field, **kwargs):
    setdefaults_path(
        kwargs,
        choices=model_field.rel.to.objects.all(),
        read_from_instance=many_to_many_factory_read_from_instance,
        extra__django_related_field=True,
    )
    kwargs['model'] = model_field.rel.to
    return Field.multi_choice_queryset(model_field=model_field, **kwargs)


_field_factory_by_field_type = OrderedDict()


def register_field_factory(field_class, factory):
    _field_factory_by_field_type[field_class] = factory


def setup_db_compat_django():
    # The order here is significant because of inheritance structure. More specific must be below less specific.
    register_field_factory(CharField, Field)
    register_field_factory(URLField, Field.url)
    register_field_factory(TimeField, Field.time)
    register_field_factory(EmailField, Field.email)
    register_field_factory(DecimalField, Field.decimal)
    register_field_factory(DateField, Field.date)
    register_field_factory(DateTimeField, Field.datetime)
    register_field_factory(CommaSeparatedIntegerField, lambda **kwargs: Field.comma_separated(parent_field=Field.integer(**kwargs)))
    register_field_factory(BooleanField, Field.boolean)
    register_field_factory(TextField, Field.text)
    register_field_factory(FloatField, Field.float)
    register_field_factory(IntegerField, Field.integer)
    register_field_factory(AutoField, lambda **kwargs: Field.integer(**setdefaults_path(kwargs, show=False)))
    register_field_factory(ManyToOneRel, None)
    register_field_factory(ManyToManyRel, None)
    register_field_factory(FileField, Field.file)
    register_field_factory(ForeignKey, foreign_key_factory)
    register_field_factory(ManyToManyField, many_to_many_factory)


def _django_field_defaults(model_field):
    r = {}
    if hasattr(model_field, 'verbose_name'):
        r['label'] = capitalize(model_field.verbose_name)

    if hasattr(model_field, 'null') and not isinstance(model_field, BooleanField):
        r['required'] = not model_field.null and not model_field.blank

    if hasattr(model_field, 'blank'):
        r['parse_empty_string_as_none'] = not model_field.blank

    return r


MISSING = object()


@dispatch
def create_members_from_model(default_factory, model, member_params_by_member_name, include=None, exclude=None, extra=None):
    def should_include(name):
        if exclude is not None and name in exclude:
            return False
        if include is not None:
            return name in include
        return True

    members = []

    # Validate include/exclude parameters
    field_names = {x.name for x in get_fields(model)}
    if include:
        assert all(x in field_names for x in include)
    if exclude:
        assert all(x in field_names for x in exclude)

    for field in get_fields(model):
        if should_include(field.name):
            subkeys = member_params_by_member_name.pop(field.name, {})
            subkeys.setdefault('class', default_factory)
            foo = subkeys.pop('class')(name=field.name, model=model, model_field=field, **subkeys)
            if foo is None:
                continue
            if isinstance(foo, list):
                members.extend(foo)
            else:
                members.append(foo)
    assert_kwargs_empty(member_params_by_member_name)
    return members + (extra if extra is not None else [])


def member_from_model(model, factory_lookup, defaults_factory, factory_lookup_register_function=None, field_name=None, model_field=None, **kwargs):
    if model_field is None:
        # noinspection PyProtectedMember
        model_field = model._meta.get_field(field_name)

    setdefaults_path(
        kwargs,
        defaults_factory(model_field),
        name=field_name,
    )

    factory = factory_lookup.get(type(model_field), MISSING)

    if factory is MISSING:
        for django_field_type, func in reversed(factory_lookup.items()):
            if isinstance(model_field, django_field_type):
                factory = func
                break

    if factory is MISSING:  # pragma: no cover
        message = 'No factory for %s.' % type(model_field)
        if factory_lookup_register_function is not None:
            message += ' Register a factory with %s, you can also register one that returns None to not handle this field type' % factory_lookup_register_function.__name__
        raise AssertionError(message)

    return factory(model_field=model_field, model=model, **kwargs) if factory else None


@dispatch(
    field=EMPTY,
)
def expand_member(model, factory_lookup, defaults_factory, name, field, field_name=None, model_field=None):
    if model_field is None:  # pragma: no cover
        # noinspection PyProtectedMember
        model_field = model._meta.get_field(field_name)
    assert isinstance(model_field, OneToOneField)

    result = [member_from_model(model=model_field.rel.to,
                                factory_lookup=factory_lookup,
                                factory_lookup_register_function=register_field_factory,
                                defaults_factory=defaults_factory,
                                field_name=sub_model_field.name,
                                name=name + '__' + sub_model_field.name,
                                **field.pop(sub_model_field.name, {}))
              for sub_model_field in get_fields(model=model_field.rel.to)]
    assert_kwargs_empty(field)
    return [x for x in result if x is not None]


def render_css_classes(classes):
    """
    Render CSS classes, or return '' if no attributes needs to be rendered.
    """
    return '' if not classes else mark_safe(' class="%s"' % ' '.join(sorted(classes)))


def default_endpoint__config(field, key, value, **_):
    # type: (Field, str, str) -> dict
    return dict(
        name=field.name,
    )


def default_endpoint__validate(field, key, value, **_):
    return dict(
        valid=not bool(field.errors),
        errors=list(field.errors),
    )


class NamespaceAwareObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            getattr(self, k)  # Check existence
            setattr(self, k, v)
        super(NamespaceAwareObject, self).__init__()


def float_parse(string_value, **_):
    try:
        return float(string_value)
    except ValueError:
        # Acrobatics so we get equal formatting in python 2/3
        raise ValueError("could not convert string to float: %s" % string_value)


def choice_is_valid(form, field, parsed_data):
    del form
    return parsed_data in field.choices, '%s not in available choices' % parsed_data


def choice_post_validation(form, field):
    def choice_tuples_lazy():
        choice_tuples = (field.choice_to_option(form=form, field=field, choice=choice) for choice in field.choices)
        if not field.required and not field.is_list:
            choice_tuples = chain([field.empty_choice_tuple], choice_tuples)
        return choice_tuples
    field.choice_tuples = choice_tuples_lazy


def choice_choice_to_option(form, field, choice):
    return choice, "%s" % choice, "%s" % choice, choice == field.value


def choice_queryset_is_valid(field, parsed_data, **_):
    return field.choices.filter(pk=parsed_data.pk).exists(), '%s not in available choices' % (field.raw_data or ', '.join(field.raw_data_list))


def choice_queryset_endpoint__select2(field, value, **_):
    limit = 10  # pragma: no mutate
    result = field.choices.filter(**{field.extra.endpoint_attr + '__icontains': value}).values_list(*['pk', field.extra.endpoint_attr])
    return [
        dict(
            id=row[0],
            text=row[1],
        )
        for row in result[:limit]
    ]


def choice_queryset_parse(field, string_value, **_):
    return field.model.objects.get(pk=string_value) if string_value else None


def choice_queryset_choice_to_option(field, choice, **_):
    return choice, choice.pk, "%s" % choice, choice == field.value


def choice_queryset_endpoint_path(form, field):
    return DISPATCH_PATH_SEPARATOR + DISPATCH_PATH_SEPARATOR.join(part for part in [form.endpoint_dispatch_prefix, 'field', field.name] if part is not None)


datetime_iso_formats = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%Y-%m-%d %H',
]


def datetime_parse(string_value, **_):
    errors = []
    for iso_format in datetime_iso_formats:
        try:
            return datetime.strptime(string_value, iso_format)
        except ValueError as e:
            errors.append('%s' % e)
    assert errors
    raise ValidationError('Time data "%s" does not match any of the formats %s' % (string_value, ', '.join('"%s"' % x for x in datetime_iso_formats)))


def datetime_render_value(value, **_):
    return value.strftime(datetime_iso_formats[0]) if value else ''


date_iso_format = '%Y-%m-%d'


def date_parse(string_value, **_):
    try:
        return datetime.strptime(string_value, date_iso_format).date()
    except ValueError as e:
        raise ValidationError(str(e))


def date_render_value(value, **_):
    return value.strftime(date_iso_format) if value else ''


time_iso_format = '%H:%M:%S'


def time_parse(string_value, **_):
    try:
        return datetime.strptime(string_value, time_iso_format).time()
    except ValueError as e:
        raise ValidationError(str(e))


def time_render_value(value, **_):
    return value.strftime(time_iso_format)


def decimal_parse(string_value, **_):
    return Decimal(string_value)


def url_parse(string_value, **_):
    return URLValidator(string_value) or string_value


def file_write_to_instance(field, instance, value):
    if value:
        Field.write_to_instance(field=field, instance=instance, value=value)


def email_parse(string_value, **_):
    return validate_email(string_value) or string_value


def phone_number_is_valid(parsed_data, **_):
    return re.match(r'^\+\d{1,3}(( |-)?\(\d+\))?(( |-)?\d+)+$', parsed_data, re.IGNORECASE), 'Please use format +<country code> (XX) XX XX. Example of US number: +1 (212) 123 4567 or +1 212 123 4567'


def multi_choice_choice_to_option(field, choice, **_):
    return choice, "%s" % choice, "%s" % choice, field.value_list and choice in field.value_list


def multi_choice_queryset_choice_to_option(field, choice, **_):
    return choice, choice.pk, "%s" % choice, field.value_list and choice in field.value_list


def render_template(request, template, context):
    """
    @type request: django.http.HttpRequest
    @type template: str|django.template.Template|django.template.backends.django.Template
    @type context: dict
    """
    from django.template import Template
    if template is None:
        return ''
    elif isinstance(template, six.string_types):
        # positional arguments here to get compatibility with django 1.8+
        return render_to_string(template, context, request=request)
    elif isinstance(template, Template):
        return template.render(RequestContext(request, context))
    else:
        # template is type django.template.backends.django.Template here
        return template.render(context, request)


def evaluate_and_group_links(links, **kwargs):
    grouped_links = {}
    if links is not None:
        links = evaluate_recursive(links, **kwargs)
        links = [link for link in links if link.show]

        grouped_links = groupby((link for link in links if link.group is not None), key=lambda l: l.group)
        grouped_links = [(g, slugify(g), list(lg)) for g, lg in grouped_links]  # list(lg) because django templates touches the generator and then I can't iterate it

        links = [link for link in links if link.group is None]

    return links, grouped_links


@six.python_2_unicode_compatible
class Link(NamespaceAwareObject):
    @dispatch(
        tag='a',
        attrs=EMPTY,
        show=True,
        extra=EMPTY,
    )
    def __init__(self, title, **kwargs):
        self.tag = None
        self.attrs = None
        self.group = None
        self.show = None
        self.template = None
        self.extra = None
        self.title = None
        super(Link, self).__init__(title=title, **kwargs)

    def render_attrs(self):
        return render_attrs(self.attrs)

    def render(self):
        if self.template:
            return render_to_string(self.template, dict(link=self))
        else:
            return format_html(u'<{tag}{attrs}>{title}</{tag}>', tag=self.tag, attrs=self.render_attrs(), title=self.title)

    def __str__(self):
        return self.render()

    @staticmethod
    @dispatch(
        icon_classes=[],
    )
    def icon(icon, title, **kwargs):
        icon_classes = kwargs.pop('icon_classes')
        icon_classes_str = ' '.join(['fa-' + icon_class for icon_class in icon_classes])
        setdefaults_path(
            kwargs,
            title=mark_safe('<i class="fa fa-%s %s"></i> %s' % (icon, icon_classes_str, title)),
        )
        return Link(**kwargs)

    @staticmethod
    @dispatch(
        tag='button',
        attrs__class__button=True,
    )
    def button(**kwargs):
        return Link(**kwargs)

    @staticmethod
    @dispatch(
        tag='input',
        attrs__type='submit',
        attrs__value='Submit',
        attrs__accesskey='s',
        title='Submit',
    )
    def submit(**kwargs):
        return Link.button(**kwargs)


@creation_ordered
class Field(NamespaceAwareObject):
    @dispatch(
        show=True,
        extra=EMPTY,
        attrs__class=EMPTY,
        parse_empty_string_as_none=True,
        required=True,
        template='tri_form/{style}_form_row.html',
        input_template='tri_form/input.html',
        label_template='tri_form/label.html',
        errors_template='tri_form/errors.html',
        is_list=False,
        is_boolean=False,
        editable=True,
        strip_input=True,
        input_type='text',
        endpoint=EMPTY,
        endpoint__config=default_endpoint__config,
        endpoint__validate=default_endpoint__validate,
    )
    def __init__(self, **kwargs):
        """
        Note that, in addition to the parameters with the defined behavior below, you can pass in any keyword argument you need yourself, including callables that conform to the protocol, and they will be added and evaluated as members.

        All these parameters can be callables, and if they are, will be evaluated with the keyword arguments form and field. The only exceptions are is_valid (which gets form, field and parsed_data), render_value (which takes form, field and value) and parse (which gets form, field, string_value). Example of using a lambda to specify a value:

        .. code:: python

            Field(id=lambda form, field: 'my_id_%s' % field.name)

        :param name: the name of the field. This is the key used to grab the data from the form dictionary (normally request.GET or request.POST)
        :param is_valid: validation function. Should return a tuple of (bool, reason_for_failure_if_bool_is_false) or raise ValidationError. Default: lambda form, field, parsed_data: (True, '')
        :param parse: parse function. Default just returns the string input unchanged: lambda form, field, string_value: string_value
        :param initial: initial value of the field
        :param attr: the attribute path to apply or get the data from. For example using "foo__bar__baz" will result in `your_instance.foo.bar.baz` will be set by the apply() function. Defaults to same as name
        :param attrs: a dict containing any custom html attributes to be sent to the input_template.
        :param id: the HTML id attribute. Default: 'id_%s' % name
        :param label: the text in the HTML label tag. Default: capitalize(name).replace('_', ' ')
        :param template: django template filename for the entire row. Normally you shouldn't need to override on this level, see input_template, label_template and error_template below. Default: 'tri_form/{style}_form_row.html'
        :param template_string: You can inline a template string here if it's more convenient than creating a file. Default: None
        :param input_template: django template filename for the template for just the input control. Default: 'tri_form/input.html'
        :param label_template: django template filename for the template for just the label tab. Default: 'tri_form/label.html'
        :param errors_template: django template filename for the template for just the errors output. Default: 'tri_form/errors.html'
        :param required: if the field is a required field. Default: True
        :param container_css_classes: extra CSS classes to set on the container (i.e. row if rendering as a table). Default: set()
        :param label_container_css_classes: default: {'description_container'}
        :param input_container_css_classes: default: set()
        :param help_text: The help text will be grabbed from the django model if specified and available. Default: lambda form, field: '' if form.model is None else form.model._meta.get_field_by_name(field.name)[0].help_text or ''

        :param editable: default: True
        :param strip_input: runs the input data through standard python .strip() before passing it to the parse function (can NOT be callable). Default: True
        :param input_type: the type attribute on the standard input HTML tag. Default: 'text'
        :param render_value: render the parsed and validated value into a string. Default just converts to unicode: lambda form, field, value: unicode(value)
        :param is_list: interpret request data as a list (can NOT be a callable). Default False
        :param read_from_instance: callback to retrieve value from edited instance. Invoked with parameters field and instance.
        :param write_to_instance: callback to write value to instance. Invoked with parameters field, instance and value.
        """

        self.name = None

        self.show = None

        self.attr = MISSING
        self.id = MISSING
        self.label = MISSING

        self.after = None

        # raw_data/raw_data contains the strings grabbed directly from the request data
        self.raw_data = None
        self.raw_data_list = None

        self.parse_empty_string_as_none = None
        self.initial = None
        self.initial_list = None
        self.template = None
        self.template_string = None
        self.attrs = None
        self.input_template = None
        self.label_template = None
        self.errors_template = None
        self.required = None

        self.is_list = None
        self.is_boolean = None
        self.model = None
        self.model_field = None

        self.editable = None
        self.strip_input = None
        self.input_type = None

        self.extra = None

        self.choice_to_option = None
        self.empty_label = None
        self.empty_choice_tuple = None
        self.choices = None
        # (Form, Field, str) -> None

        self.endpoint = None
        self.endpoint_path = None

        super(Field, self).__init__(**kwargs)

        # Bound field data
        self.form = None
        self.field = None
        self.errors = None

        # parsed_data/parsed_data contains data that has been interpreted, but not checked for validity or access control
        self.parsed_data = None
        self.parsed_data_list = None

        # value/value_data_list is the final step that contains parsed and valid data
        self.value = None
        self.value_list = None

        self.choice_tuples = None

    @staticmethod
    def is_valid(form, field, parsed_data):
        # type: (Form, Field, object) -> (bool, str)
        return True, ''

    @staticmethod
    def parse(form, field, string_value, **_):
        # type: (Form, Field, unicode) -> object
        del form, field
        return string_value

    @staticmethod
    def container_css_classes(form, field, **_):
        # type: (Form, Field) -> set
        return set()

    @staticmethod
    def label_container_css_classes(form, field, **_):
        return {'description_container'}

    @staticmethod
    def input_container_css_classes(form, field, **_):
        # type: (Form, Field) -> set
        return set()

    @staticmethod
    def post_validation(form, field, **_):
        # type: (Form, Field) -> None
        pass

    @staticmethod
    def render_value(form, field, value):
        # type: (Form, Field, object) -> unicode
        return "%s" % value

    # grab help_text from model if applicable
    # noinspection PyProtectedMember
    @staticmethod
    def help_text(field, **_):
        if field.model is None or field.attr is None:
            return ''
        try:
            return field.model._meta.get_field(field.attr.rsplit('__', 1)[-1]).help_text or ''
        except FieldDoesNotExist:  # pragma: no cover
            return ''

    @staticmethod
    def read_from_instance(field, instance):
        # type: (Field, object) -> None
        return getattr_path(instance, field.attr)

    @staticmethod
    def write_to_instance(field, instance, value):
        # type: (Field, object, object) -> None
        setattr_path(instance, field.attr, value)

    @staticmethod
    def endpoint_dispatch(field, key, **kwargs):
        parts = key.split(DISPATCH_PATH_SEPARATOR, 1)
        prefix = parts.pop(0)
        remaining_key = parts[0] if parts else ''
        endpoint = field.endpoint.get(prefix, None)
        if endpoint is not None:
            return endpoint(field=field, key=remaining_key, **kwargs)

    """
    An internal class that is used to handle the mutable data used during parsing and validation of a Field.

    The life cycle of the data is:
        1. raw_data/raw_data_list: will be set if the corresponding key is present in the HTTP request
        2. parsed_data/parsed_data_list: set if parsing is successful, which only happens if the previous step succeeded
        3. value/value_list: set if validation is successful, which only happens if the previous step succeeded

    The variables *_list should be used if the input is a list.
    """
    def _bind(self, form):
        bound_field = copy.copy(self)  # type: Field

        if bound_field.attr is MISSING:
            bound_field.attr = bound_field.name
        if bound_field.id is MISSING:
            bound_field.id = 'id_%s' % bound_field.name if bound_field.name else ''
        if bound_field.label is MISSING:
            bound_field.label = capitalize(bound_field.name).replace('_', ' ') if bound_field.name else ''

        bound_field.form = form
        bound_field.field = self
        bound_field.errors = set()

        if form.editable is False:
            bound_field.editable = False

        return bound_field

    EVALUATED_ATTRIBUTES = {
        'after', 'attr', 'attrs', 'choice_to_option', 'choice_tuples', 'choices', 'container_css_classes', 'editable', 'empty_choice_tuple', 'empty_label', 'endpoint', 'endpoint_dispatch', 'endpoint_path', 'errors_template', 'extra', 'help_text', 'id', 'initial', 'initial_list', 'input_container_css_classes', 'input_template', 'input_type', 'is_boolean', 'is_list', 'is_valid', 'label', 'label_container_css_classes', 'label_template', 'model', 'model_field', 'parse', 'parse_empty_string_as_none', 'raw_data', 'raw_data_list', 'render_value', 'required', 'show', 'strip_input', 'template', 'template_string'
    }

    def _evaluate(self):
        """
        Evaluates callable/lambda members. After this function is called all members will be values.
        """
        for k in Field.EVALUATED_ATTRIBUTES:
            v = getattr(self, k)
            new_value = evaluate_recursive(v, form=self.form, field=self)
            if new_value is not v:
                setattr(self, k, new_value)

        if not self.editable:
            self.input_template = 'tri_form/non_editable.html'

    def rendered_value(self):
        if self.errors:
            return self.raw_data
        else:
            return self.render_value(form=self.form, field=self, value=self.value if self.value else '')

    def render_attrs(self):
        """
        Render HTML attributes, or return '' if no attributes needs to be rendered.
        """
        return render_attrs(self.attrs)

    def render_container_css_classes(self):
        container_css_classes = set(self.container_css_classes)
        if self.required and self.editable:
            container_css_classes.add('required')
        if self.form.style == 'compact':
            container_css_classes.add('key-value')
        return render_css_classes(container_css_classes)

    def render_label_container_css_classes(self):
        return render_css_classes(self.label_container_css_classes)

    def render_input_container_css_classes(self):
        return render_css_classes(self.input_container_css_classes)

    def __repr__(self):
        return '<{}.{} {}>'.format(self.__class__.__module__, self.__class__.__name__, self.name)

    """
    Class that describes a field, i.e. what input controls to render, the label, etc.
    """

    @staticmethod
    def hidden(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='hidden',
        )
        return Field(**kwargs)

    @staticmethod
    def text(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='text',
        )
        return Field(**kwargs)

    @staticmethod
    def textarea(**kwargs):
        setdefaults_path(
            kwargs,
            input_template='tri_form/text.html',
        )
        return Field(**kwargs)

    @staticmethod
    def integer(**kwargs):
        def int_parse(string_value, **_):
            return int(string_value)

        setdefaults_path(
            kwargs,
            parse=int_parse,
        )
        return Field(**kwargs)

    @staticmethod
    def float(**kwargs):
        setdefaults_path(
            kwargs,
            parse=float_parse,
        )
        return Field(**kwargs)

    @staticmethod
    def password(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='password',
        )
        return Field(**kwargs)

    @staticmethod
    def boolean(**kwargs):
        """
        Boolean field. Tries hard to parse a boolean value from its input.
        """
        setdefaults_path(
            kwargs,
            parse=lambda string_value, **_: bool_parse(string_value),
            required=False,
            template='tri_form/{style}_form_row_checkbox.html',
            input_template='tri_form/checkbox.html',
            is_boolean=True,
        )
        return Field(**kwargs)

    @staticmethod
    def choice(**kwargs):
        """
        Shortcut for single choice field. If required is false it will automatically add an option first with the value '' and the title '---'. To override that text pass in the parameter empty_label.
        :param empty_label: default '---'
        :param choices: list of objects
        :param choice_to_option: callable with three arguments: form, field, choice. Convert from a choice object to a tuple of (choice, value, label, selected), the last three for the <option> element
        """
        assert 'choices' in kwargs

        setdefaults_path(
            kwargs,
            required=True,
            is_list=False,
            empty_label='---',
        )

        if not kwargs['required'] and not kwargs['is_list']:
            original_parse = kwargs.get('parse', Field.parse)

            def parse(form, field, string_value):
                return original_parse(form=form, field=field, string_value=string_value)

            kwargs.update(
                parse=parse
            )

        setdefaults_path(
            kwargs,
            empty_choice_tuple=(None, '', kwargs['empty_label'], True),
            choice_to_option=choice_choice_to_option,
            input_template='tri_form/choice.html',
            is_valid=choice_is_valid,
            post_validation=choice_post_validation,
        )

        return Field(**kwargs)

    @staticmethod
    def choice_queryset(**kwargs):
        kwargs = setdefaults_path(
            Struct(),
            kwargs,
            parse=choice_queryset_parse,
            choice_to_option=choice_queryset_choice_to_option,
            endpoint_path=choice_queryset_endpoint_path,
            endpoint__=choice_queryset_endpoint__select2,  # Backwards compatible
            endpoint__select2=choice_queryset_endpoint__select2,
            extra__endpoint_attr='name',
            is_valid=choice_queryset_is_valid,
        )
        return Field.choice(**kwargs)

    @staticmethod
    def multi_choice(**kwargs):
        setdefaults_path(
            kwargs,
            attrs__multiple=True,
            choice_to_option=multi_choice_choice_to_option,
            is_list=True,
        )
        return Field.choice(**kwargs)

    @staticmethod
    def multi_choice_queryset(**kwargs):
        setdefaults_path(
            kwargs,
            attrs__multiple=True,
            choice_to_option=multi_choice_queryset_choice_to_option,
            is_list=True,
        )
        return Field.choice_queryset(**kwargs)

    @staticmethod
    def radio(**kwargs):
        setdefaults_path(
            kwargs,
            input_template='tri_form/radio.html',
        )
        return Field.choice(**kwargs)

    @staticmethod
    def datetime(**kwargs):
        setdefaults_path(
            kwargs,
            parse=datetime_parse,
            render_value=datetime_render_value,
        )
        return Field(**kwargs)

    @staticmethod
    def date(**kwargs):
        setdefaults_path(
            kwargs,
            parse=date_parse,
            render_value=date_render_value,
        )
        return Field(**kwargs)

    @staticmethod
    def time(**kwargs):
        setdefaults_path(
            kwargs,
            parse=time_parse,
            render_value=time_render_value,
        )
        return Field(**kwargs)

    @staticmethod
    def decimal(**kwargs):
        setdefaults_path(
            kwargs,
            parse=decimal_parse,
        )
        return Field(**kwargs)

    @staticmethod
    def url(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='url',
            parse=url_parse,
        )
        return Field(**kwargs)

    @staticmethod
    def file(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='file',
            template_string='{% extends "tri_form/table_form_row.html" %}{% block extra_content %}{{ field.value }}{% endblock %}',
            write_to_instance=file_write_to_instance,
        )
        return Field(**kwargs)

    @staticmethod
    def heading(label, show=True, template='tri_form/heading.html', **kwargs):
        """
        Shortcut to create a fake input that performs no parsing but is useful to separate sections of a form.
        """
        setdefaults_path(
            kwargs,
            label=label,
            show=show,
            template=template,
            editable=False,
            attr=None,
            name='@@heading@@',
        )
        return Field(**kwargs)

    @staticmethod
    def info(value, **kwargs):
        """
        Shortcut to create an info entry.
        """
        setdefaults_path(
            kwargs,
            initial=value,
            editable=False,
            attr=None,
        )
        return Field(**kwargs)

    @staticmethod
    def email(**kwargs):
        setdefaults_path(
            kwargs,
            input_type='email',
            parse=email_parse,
        )
        return Field(**kwargs)

    @staticmethod
    def phone_number(**kwargs):
        setdefaults_path(
            kwargs,
            is_valid=phone_number_is_valid,
        )
        return Field(**kwargs)

    @staticmethod
    def from_model(model, field_name=None, model_field=None, **kwargs):
        return member_from_model(
            model=model,
            factory_lookup=_field_factory_by_field_type,
            factory_lookup_register_function=register_field_factory,
            defaults_factory=_django_field_defaults,
            field_name=field_name,
            model_field=model_field,
            **kwargs)

    @staticmethod
    def from_model_expand(model, field_name=None, model_field=None, **kwargs):
        return expand_member(
            model=model,
            factory_lookup=_field_factory_by_field_type,
            defaults_factory=_django_field_defaults,
            field_name=field_name,
            model_field=model_field,
            **kwargs)

    @staticmethod
    def comma_separated(parent_field):
        """
        Shortcut to create a comma separated list of something. You can use this to create a comma separated text input that gives nice validation errors easily. Example:

        .. code:: python

            Field.comma_separated(Field.email)

        :type parent_field: Field
        """
        new_field = copy.copy(parent_field)

        def parse_comma_separated(form, field, string_value):
            errors = []
            result = []
            for x in string_value.split(','):
                x = x.strip()
                try:
                    result.append(parent_field.parse(form=form, field=field, string_value=x.strip()))
                except ValueError as e:
                    errors.append('Invalid value "%s": %s' % (x, e))
                except ValidationError as e:
                    for message in e.messages:
                        errors.append('Invalid value "%s": %s' % (x, message))
            if errors:
                raise ValidationError(errors)
            return ', '.join(result)
        new_field.parse = parse_comma_separated

        def is_valid_comma_separated(form, field, parsed_data):
            errors = set()
            for x in parsed_data.split(','):
                x = x.strip()
                is_valid, error = parent_field.is_valid(form=form, field=field, parsed_data=x)
                if not is_valid:
                    errors.add('Invalid value "%s": %s' % (x, error))
            return errors == set(), errors
        new_field.is_valid = is_valid_comma_separated

        return new_field


def get_fields(model):
    # noinspection PyProtectedMember
    for field in model._meta.get_fields():
        yield field


def default_endpoint__field(form, key, value):
    parts = key.split('__', 1)
    prefix = parts.pop(0)
    remaining_key = parts[0] if parts else ''
    field = form.fields_by_name.get(prefix, None)
    if field is not None:
        return field.endpoint_dispatch(form=form, field=field, key=remaining_key, value=value)


@python_2_unicode_compatible
@declarative(Field, 'fields_dict')
@with_meta
class Form(NamespaceAwareObject):
    """
    Describe a Form. Example:

    .. code:: python

        class MyForm(Form):
            a = Field()
            b = Field.email()

        form = MyForm(data={})

    You can also create an instance of a form with this syntax if it's more convenient:

    .. code:: python

        form = MyForm(data={}, fields=[Field(name='a'), Field.email(name='b')])

    See tri.declarative docs for more on this dual style of declaration.
    """
    @dispatch(
        is_full_form=True,
        model=None,
        endpoint__field=default_endpoint__field,
        editable=True,
        extra=EMPTY,
        attrs__class__newforms=True,
        attrs__action='',
        attrs__method='post',
        links=[Link.submit()],
        links_template='tri_form/links.html',
    )
    def __init__(self, request=None, data=None, instance=None, fields=None, fields_dict=None, **kwargs):
        """
        :type fields: list of Field
        :type data: dict[basestring, any]
        :type model: django.db.models.Model
        """
        self.is_full_form = None
        self.links = None
        self.links_template = None
        self.attrs = None
        self.editable = None
        self.name = None

        self.model = None
        """ :type: django.db.models.Model """
        self.endpoint_dispatch_prefix = None
        """ :type: str """
        self.endpoint = None
        """ :type: tri.declarative.Namespace """
        self.extra = None
        """ :type: tri.declarative.Namespace """
        super(Form, self).__init__(**kwargs)

        self.request = request

        if data is None and request:
            data = request.POST if request.method == 'POST' else request.GET

        if data is None:
            data = {}

        self.data = data

        def unbound_fields():
            if fields is not None:
                for field in fields:
                    yield field
            for name, field in fields_dict.items():
                setattr(field, 'name', name)
                yield field
        self.fields = sort_after([f._bind(self) for f in unbound_fields()])
        """ :type: list of Field"""

        if instance is not None:
            for field in self.fields:
                if field.attr:
                    initial = field.read_from_instance(field, instance)
                    if field.is_list:
                        field.initial_list = initial
                    else:
                        field.initial = initial

            self.instance = instance
        else:
            self.instance = None

        self.mode = FULL_FORM_FROM_REQUEST if '-' in data else INITIALS_FROM_GET
        if request and request.method == 'POST' and self.is_target():
            self.mode = FULL_FORM_FROM_REQUEST

        if self.mode == INITIALS_FROM_GET and request and self.is_target():
            assert request.method == 'GET', 'Seems to be a POST but parameter "-" is not present'

        if data:
            for field in self.fields:
                if field.is_list:
                    if field.raw_data_list is not None:
                        continue
                    try:
                        # django and similar
                        # noinspection PyUnresolvedReferences
                        raw_data_list = data.getlist(field.name)
                    except AttributeError:  # pragma: no cover
                        # werkzeug and similar
                        raw_data_list = data.get(field.name)

                    if raw_data_list and field.strip_input:
                        raw_data_list = [x.strip() for x in raw_data_list]

                    if raw_data_list is not None:
                        field.raw_data_list = raw_data_list
                else:
                    if field.raw_data is not None:
                        continue
                    field.raw_data = data.get(field.name)
                    if field.raw_data and field.strip_input:
                        field.raw_data = field.raw_data.strip()

        self.fields_by_name = None
        """ :type: dict[str, Field] """
        self.style = None
        self.errors = set()
        """ :type: set of str """
        self._valid = None
        self.evaluate()
        self.is_valid()

    def render_attrs(self):
        """
        Render HTML attributes, or return '' if no attributes needs to be rendered.
        """
        return render_attrs(self.attrs)

    def render_links(self):
        links, grouped_links = evaluate_and_group_links(self.links)
        return render_template(self.request, self.links_template, dict(links=links, grouped_links=grouped_links, form=self))

    @staticmethod
    @dispatch(
        field=EMPTY,
    )
    def fields_from_model(field, **kwargs):
        return create_members_from_model(
            member_params_by_member_name=field,
            default_factory=Field.from_model,
            **kwargs
        )

    @staticmethod
    @dispatch(
        field=EMPTY,
    )
    def from_model(data, model, field, instance=None, include=None, exclude=None, extra_fields=None, **kwargs):
        """
        Create an entire form based on the fields of a model. To override a field parameter send keyword arguments in the form
        of "the_name_of_the_field__param". For example:

        .. code:: python

            class Foo(Model):
                foo = IntegerField()

            Form.from_model(data=request.GET, model=Foo, field__foo__help_text='Overridden help text')

        :param include: fields to include. Defaults to all
        :param exclude: fields to exclude. Defaults to none (except that AutoField is always excluded!)

        """
        fields = Form.fields_from_model(model=model, include=include, exclude=exclude, extra=extra_fields, field=field)
        return Form(data=data, model=model, instance=instance, fields=fields, **kwargs)

    def is_target(self):
        if not self.name:
            return True
        return self.name in self.data

    def is_valid(self):
        if self._valid is None:
            self.validate()
            for field in self.fields:
                if field.errors:
                    self._valid = False
                    break
            else:
                self._valid = not self.errors
        return self._valid

    def parse_field_raw_value(self, field, raw_data):
        try:
            return field.parse(form=self, field=field, string_value=raw_data)
        except ValueError as e:
            assert str(e) != ''
            field.errors.add(str(e))
        except ValidationError as e:
            for message in e.messages:
                msg = "%s" % message
                assert msg != ''
                field.errors.add(msg)

    def parse(self):
        for field in self.fields:
            if not field.editable:
                continue

            if self.mode is INITIALS_FROM_GET and field.raw_data is None and field.raw_data_list is None:
                continue

            if field.is_list:
                if field.raw_data_list is not None:
                    field.parsed_data_list = [self.parse_field_raw_value(field, x) for x in field.raw_data_list]
                else:
                    field.parsed_data_list = None
            elif field.is_boolean:
                field.parsed_data = self.parse_field_raw_value(field, '0' if field.raw_data is None else field.raw_data)
            else:
                if field.raw_data == '' and field.parse_empty_string_as_none:
                    field.parsed_data = None
                elif field.raw_data is not None:
                    field.parsed_data = self.parse_field_raw_value(field, field.raw_data)
                else:
                    field.parsed_data = None

    def evaluate(self):
        for field in self.fields:
            field._evaluate()
        self.fields = [field for field in self.fields if should_show(field)]
        self.fields_by_name = Struct({field.name: field for field in self.fields})

    def validate(self):
        self.parse()

        for field in self.fields:
            if (not field.editable) or (self.mode is INITIALS_FROM_GET and field.raw_data is None and field.raw_data_list is None):
                if field.is_list:
                    field.value_list = field.initial_list
                else:
                    field.value = field.initial
                continue

            value = None
            value_list = None
            if field.is_list:
                if field.parsed_data_list is not None:
                    value_list = [self.validate_field_parsed_data(field, x) for x in field.parsed_data_list if x is not None]
            else:
                if field.parsed_data is not None:
                    value = self.validate_field_parsed_data(field, field.parsed_data)

            if not field.errors:
                if self.mode is FULL_FORM_FROM_REQUEST and field.required and value in [None, ''] and not value_list:
                    field.errors.add('This field is required')
                else:
                    field.value = value
                    field.value_list = value_list

        for field in self.fields:
            field.post_validation(form=self, field=field)
        self.post_validation(form=self)
        return self

    @staticmethod
    def post_validation(form):
        pass

    def validate_field_parsed_data(self, field, value):
        is_valid, error = field.is_valid(
            form=self,
            field=field,
            parsed_data=value)
        if is_valid and not field.errors and field.parsed_data is not None:
            value = field.parsed_data
        elif not is_valid and self.mode:
            if not isinstance(error, set):
                error = {error}
            for e in error:
                assert error != ''
                field.errors.add(e)
        return value

    def add_error(self, msg):
        self.errors.add(msg)

    def __str__(self):
        return self.table()

    def compact(self):
        return self.render(template_name=None)

    def table(self):
        return self.render(style='table', template_name=None)

    def render(self, style='compact', template_name="tri_form/form.html"):
        """
        :type style: str| unicode
        :type template_name: str | unicode | None
        """
        self.style = style
        r = []
        for field in self.fields:
            context = {
                'form': self,
                'field': field,
            }
            if field.template_string is not None:
                r.append(get_template_from_string(field.template_string, origin='tri.form', name='Form.render').render(context, self.request))
            else:
                r.append(render_to_string(field.template.format(style=style), context))
        if self.is_full_form:
            r.append(AVOID_EMPTY_FORM)

        if template_name is None:
            return mark_safe('\n'.join(r))
        else:
            return render_to_string(
                template_name=template_name,
                context=dict(form=self),
                request=self.request
            )

    def apply(self, instance):
        """
        Write the new values specified in the form into the instance specified.
        """
        assert self.is_valid()
        for field in self.fields:
            self.apply_field(instance=instance, field=field)
        return instance

    @staticmethod
    def apply_field(instance, field):
        if not field.editable:
            field.value = field.initial
            field.value_list = field.initial_list

        if field.attr is not None:
            field.write_to_instance(field, instance, field.value_list if field.is_list else field.value)

    def get_errors(self):
        r = {}
        if self.errors:
            r['global'] = self.errors
        field_errors = {x.name: x.errors for x in self.fields if x.errors}
        if field_errors:
            r['fields'] = field_errors
        return r

    def endpoint_dispatch(self, key, value):
        parts = key.split(DISPATCH_PATH_SEPARATOR, 1)
        prefix = parts.pop(0)
        remaining_key = parts[0] if parts else ''
        handler = self.endpoint.get(prefix, None)
        if handler is not None:
            return handler(form=self, key=remaining_key, value=value)


# Backward compatibility
default_read_from_instance = Field.read_from_instance
default_write_to_instance = Field.write_to_instance

setup_db_compat_django()
