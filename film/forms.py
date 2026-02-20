from django import forms
from .models import Category, Genre, Film

not_valid_word = ["name", 'xxx', 'admin']

class AddFilmForm(forms.ModelForm):

    class Meta:
        model = Film
        fields = ["name", "descriptions", "year", "image"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name:
            for word in not_valid_word:
                if word in name:
                    raise forms.ValidationError("Это слово запрещено!!!")

        return cleaned_data
    
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