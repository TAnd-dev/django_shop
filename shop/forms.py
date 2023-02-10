from django import forms

from shop.models import Review

SORT = [
    ('1', 'Сначала недорогие'),
    ('2', 'Сначала дорогие'),
    ('3', 'Сначала популярные'),
    ('4', 'Сначала обсуждаемые'),
    ('5', 'Сначала с лучшей оценкой')
]


class FilterProducts(forms.Form):
    min_price = forms.IntegerField(
        label='Минимальная цена',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )
    max_price = forms.IntegerField(
        label='Максимальная цена',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '999999'})
    )
    sort = forms.ChoiceField(
        label='Сортировка',
        widget=forms.RadioSelect,
        required=False,
        choices=SORT
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate', 'text')
        widgets = {
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
