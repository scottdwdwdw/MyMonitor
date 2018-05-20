#from django.contrib import admin

# Register your models here.

from django import forms
from monitor import models
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
import xadmin


class UserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    name = forms.CharField(label='username',widget=forms.TextInput)
    email = forms.EmailField(label='email',widget=forms.EmailInput)

    class Meta:
        model = models.UserProfile
        fields = ('name', 'email', 'memo', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def is_valid(self):
        return self.is_bound and not self.errors

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField(label="Password",
    #     #                                      help_text=("Raw passwords are not stored, so there is no way to see "
    #     #                                                 "this user's password, but you can change the password "
    #     #                                                 "using <a href=\"password/\">this form</a>."))

    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('name', 'email',  'password', 'is_active', 'is_admin', 'is_staff', 'memo')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    change_user_password_template = None
    list_display = ('name', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    list_editable = ['is_admin']
    search_fields = ('name', 'email')
    ordering = ('name',)

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('','name', 'password',css_class='unsort no_title' ),
                    Fieldset('Personal info','email', 'memo'),
                    Fieldset('Status', 'is_active', 'is_staff'),
                )
            )
        else:
            self.form_layout=(
                Main(
                    Fieldset('', 'name', 'password1', 'password2',css_class='unsort no_title'),
                    Fieldset('Personal info', 'email', 'memo'),
                    Fieldset('Status', 'is_admin')
                )
            )
        return super(UserAdmin, self).get_form_layout()





class HostAdmin(object):
    list_display =  ('id','name','ip_addr','status')
    filter_horizontal = ('host_groups','templates')


class TemplateAdmin(object):
    filter_horizontal = ('services','triggers')

class ServiceAdmin(object):
    filter_horizontal = ('items',)
    list_display = ('name','interval','plugin_name')
    #list_select_related = ('items',)


class TriggerExpressionInline(object):
    model = models.TriggerExpression
    #exclude = ('memo',)
    #readonly_fields = ['create_date']


class TriggerAdmin(object):
    list_display = ('name','severity','enabled')
    inlines = [TriggerExpressionInline,]
    #filter_horizontal = ('expressions',)


class TriggerExpressionAdmin(object):
    list_display = ('trigger','service','service_index','specified_index_key','operator_type','data_calc_func','threshold','logic_type')


xadmin.site.register(models.UserProfile, UserProfileAdmin)
xadmin.site.register(models.Host, HostAdmin)
xadmin.site.register(models.HostGroup)
xadmin.site.register(models.Template, TemplateAdmin)
xadmin.site.register(models.Service, ServiceAdmin)
xadmin.site.register(models.ServiceIndex)
xadmin.site.register(models.Trigger, TriggerAdmin)
xadmin.site.register(models.TriggerExpression, TriggerExpressionAdmin)
xadmin.site.register(models.Action)
xadmin.site.register(models.ActionOperation)
#admin.site.register(models.ActionCondtion,ActionConditionAdmin)
xadmin.site.register(models.Maintenance)
xadmin.site.register(models.EventLog)


