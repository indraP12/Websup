from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'password')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email','name', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class PlanAdmin(admin.ModelAdmin):
	model = Plan
	list_display = ("name_of_plan", "credits", "price", "duration", "is_active")


class User_PlanAdmin(admin.ModelAdmin):
	model = User_Plan
	list_display = ("user", "plan", "started_on" ,"paid_amount" ,"total_credits", "used_credits", "remaining_credits", "ending_on")


class ContactAdmin(admin.ModelAdmin):
	model = Contact
	list_display = ("number",)


class WhatsappFormatAdmin(admin.ModelAdmin):
	model = WhatApp_Message_Format
	list_display = ("campaign_name", "from_user", "sent_on", "msg_text")


class WhatsappindividualmsgAdmin(admin.ModelAdmin):
	model = WhatsApp_Individual_Message
	list_display = ("to_contact", "message_format", "delivered", "sent_using", "sent_on")


class contactusAdmin(admin.ModelAdmin):
    model = contactus
    list_display = ("name", "contact_number", "email_address", "contact_msg")

admin.site.register(MyUser, UserAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(User_Plan, User_PlanAdmin)
admin.site.register(WhatsApp_Individual_Message, WhatsappindividualmsgAdmin)
admin.site.register(WhatApp_Message_Format, WhatsappFormatAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(contactus, contactusAdmin)
admin.site.unregister(Group)