from django import forms
from django.contrib import admin
from .models import Email, Show, User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class PersonalityContestAdminSite(admin.AdminSite):
	site_title = 'Personality Contest'
	site_header = 'Personality Contest Admin'

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ['email',]
    ordering = ['email',]
    filter_horizontal = ()


class ShowAdmin(admin.ModelAdmin):

    list_display = ('city', 'state', 'venue', 'date', 'start')
    list_filter = ('city', 'state', 'date', 'venue')
    fieldsets = (
        ('When', {'fields': ('date', 'start', 'end', 'play_time')}),
        ('Where', {'fields': ('city','state', 'venue')}),
    )

    search_fields = ['date', 'city', 'state', 'location',]
    ordering = ['date','start']
    filter_horizontal = ()
    class Meta:
        model = Show

class EmailAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm
    readonly_fields = ('approved',)

    list_display = ('subject', 'send_date', )
    list_filter = ('approved',)

    search_fields = ['subject',]
    ordering = ['send_date',]
    class Meta:
        model = Email

admin_site = PersonalityContestAdminSite()

admin_site.register(Show, ShowAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Email, EmailAdmin)
