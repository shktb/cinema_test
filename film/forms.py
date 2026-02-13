from django import forms
from .models import Category, Genre

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
    
class SearchForm(forms.Form):
    for_test_list = [("1", "Комедия"), ("2", "Фэнтези")]
    year_list = [("0", "..."), ("1", "Больше 2000"), ("2", "меньше 2000")]
    search = forms.CharField(required=False)
    category_id = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False
    )
    year_choice = forms.ChoiceField(choices=year_list, required=False)
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False)
    for_test = forms.MultipleChoiceField(choices=for_test_list, required=False)