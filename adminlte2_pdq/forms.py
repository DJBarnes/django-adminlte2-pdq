"""Django AdminLTE2 Sample Forms"""
from django import forms

CHOICES = (
    (1, 'foo'),
    (2, 'bar'),
)

class SampleForm(forms.Form):
    """Sample Form with all field types"""
    sample_bool = forms.BooleanField()
    sample_char = forms.CharField()
    sample_phone = forms.CharField()
    sample_range = forms.CharField()
    sample_color = forms.CharField()
    sample_datalist = forms.CharField()
    sample_range_datalist = forms.CharField()
    sample_choice = forms.ChoiceField(choices=CHOICES)
    sample_date = forms.DateField()
    sample_date_time = forms.DateTimeField()
    sample_decimal = forms.DecimalField()
    sample_duration = forms.DurationField()
    sample_email = forms.EmailField()
    sample_file = forms.FileField()
    sample_file_path = forms.FilePathField('./')
    sample_float = forms.FloatField()
    sample_generic_ip = forms.GenericIPAddressField()
    sample_integer = forms.IntegerField()
    try:
        # Fails for Django < 3.0. Skip if so.
        sample_json = forms.JSONField()
    except:
        pass
    sample_multi_choice = forms.MultipleChoiceField(choices=CHOICES)
    sample_null_bool = forms.NullBooleanField()
    sample_regex = forms.RegexField(r's*')
    sample_slug = forms.SlugField()
    sample_time = forms.TimeField()
    sample_typed_choice = forms.TypedChoiceField(choices=CHOICES, coerce=int)
    sample_typed_multi_choice = forms.TypedMultipleChoiceField(choices=CHOICES, coerce=int)
    sample_url = forms.URLField()
    sample_uuid = forms.UUIDField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['sample_range_datalist'].range_min_max = {'min':5, 'max':9}
        self['sample_range_datalist'].datalist = {'name':'my_range_datalist', 'data':[5,7,9]}
