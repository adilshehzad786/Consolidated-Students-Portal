from django import forms
from portal.models import EmailUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class EmailUserCreationForm(forms.ModelForm):

  error_messages = {
  'duplicate_email': _("A user with that email already exists."),
  'password_mismatch': _("The two password fields didn't match."),
  }
  password1 = forms.CharField(
  label=_("Password"),
  widget=forms.PasswordInput)
  password2 = forms.CharField(
  label=_("Password confirmation"),
  widget=forms.PasswordInput,
  help_text=_("Enter the same password as above, for verification."))
  class Meta:
    model = get_user_model()
    fields = ('email',)

  def clean_email(self):
    email = self.cleaned_data["email"]
    try:
      get_user_model()._default_manager.get(email=email)
    except get_user_model().DoesNotExist:
      return email
    raise forms.ValidationError(
      self.error_messages['duplicate_email'],
      code='duplicate_email',
    )

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError(
      self.error_messages['password_mismatch'],
      code='password_mismatch',
    )
    return password2

  def save(self, commit=True):
    user = super(EmailUserCreationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user

class EmailUserChangeForm(forms.ModelForm):
  password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
    "Raw passwords are not stored, so there is no way to see "
    "this user's password, but you can change the password "
    "using <a href=\"password/\">this form</a>."))
  
  class Meta:
    model = get_user_model()
    exclude = ()

  def __init__(self, *args, **kwargs):
    super(EmailUserChangeForm, self).__init__(*args, **kwargs)
    f = self.fields.get('user_permissions', None)
    if f is not None:
      f.queryset = f.queryset.select_related('content_type')

  def clean_password(self):
    return self.initial["password"]
