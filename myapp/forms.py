from django import forms
from .models import result
from .models import title
from .models import owner
from .models import title, contract, project


class AnswerForm(forms.ModelForm):
    class Meta:
        model=result
        fields=( 'owner_id','result','problem','solution')
class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = title
        fields = ('title_name',)

    project_id = forms.ModelChoiceField(queryset=project.objects.all())
    contract_no = forms.CharField()

    def save(self, commit=True):
        title_obj = super().save(commit=False)
        project_id = self.cleaned_data.get('project_id')
        contract_no = self.cleaned_data.get('contract_no')
        contract_obj = contract.objects.create(project_id=project_id, contract_no=contract_no)
        title_obj.contract_id = contract_obj
        if commit:
            title_obj.save()
        if hasattr(title_obj, 'user'):
            owner_obj = owner.objects.create(title_id=title_obj, depcode='DEP', template='TMP')
            if commit:
                owner_obj.save()
        return title_obj
class OwnerForm(forms.ModelForm):
    class Meta:
        model = owner
        fields = ('owner_id', 'title_id')
class projectForm(forms.ModelForm):
    class Meta:
        model = project
        fields = ('project_id', 'project_name','project_year_start','project_year_end')


    
        