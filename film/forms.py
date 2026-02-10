from django import forms
not_valid_word = ["name", 'xxx', 'admin']

class AddFilmForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    year = forms.IntegerField()
    image = forms.ImageField()
    
    def clear(self):
        data = self.cleaned_data
        name = data.get('name')
        if name in not_valid_word:
            raise forms.ValidationError('Это слово запрещено!!!')
        return data