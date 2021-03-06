from django import forms
from provider_registration.validators import URLResolves


from provider_registration.models import RegistrationInfo


class InitialProviderForm(forms.ModelForm):
    base_url = forms.CharField(max_length=100, validators=[URLResolves()])
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'description',
                  'oai_provider', 'reg_id']


class ContactInfoForm(forms.ModelForm):
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['contact_name', 'contact_email', 'reg_id']


class MetadataQuestionsForm(forms.ModelForm):
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['meta_tos', 'meta_privacy', 'meta_sharing_tos',
                  'meta_license', 'meta_license_extended',
                  'meta_future_license', 'reg_id']


class OAIProviderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(OAIProviderForm, self).__init__(*args, **kwargs)
        self.fields['approved_sets'].choices = self.choices

    provider_long_name = forms.CharField(widget=forms.HiddenInput())
    reg_id = forms.CharField(widget=forms.HiddenInput())
    base_url = forms.URLField()

    property_list = forms.CharField(widget=forms.Textarea)
    approved_sets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url',
                  'property_list', 'approved_sets', 'reg_id']


class OtherProviderForm(forms.ModelForm):
    provider_long_name = forms.CharField(widget=forms.HiddenInput())
    reg_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = RegistrationInfo
        fields = ['provider_long_name', 'base_url', 'property_list', 'reg_id']
