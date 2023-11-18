from django.contrib import admin
from .models import Competition, Federation, Participant, Region

from django import forms
from django.contrib import admin
from .models import Competition

class CompetitionAdminForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].required = False 

        if 'competition_type' in self.data:
            competition_type = self.data['competition_type']
            if competition_type == 'regional':
                self.fields['region'].required = True

# class CompetitionAdminForm(forms.ModelForm):
#     class Meta:
#         model = Competition
#         fields = '__all__'  # or list the fields you want to include

#     def __init__(self, *args, **kwargs):
#         super(CompetitionAdminForm, self).__init__(*args, **kwargs)
#         # Initially hide the region field
#         self.fields['region'].widget = forms.HiddenInput()

#         # If the instance has a competition_type of 'regional', show the field
#         if self.instance.competition_type == 'regional':
#             self.fields['region'].widget = forms.Select(choices=self.fields['region'].choices)

class CompetitionAdmin(admin.ModelAdmin):
    form = CompetitionAdminForm
    change_form_template = 'admin/competition/change_form.html'
    list_display = ['name', 'start_date', 'end_date', 'address', 'organizator', 'federation', 'competition_type', 'region']
    list_filter = ['competition_type', 'region']

    class Media:
        js = (
            'admin/competition/admin_add_competition.js',
        )

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Federation)
admin.site.register(Participant)
admin.site.register(Region)