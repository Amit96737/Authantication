from django import forms

class NewsFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', '🌍 All News'),
        ('business', '💼 Business'),
        ('technology', '💻 Technology'),
        ('sports', '⚽ Sports'),
        ('science', '🔬 Science'),
        ('health', '🏥 Health'),
        ('entertainment', '🎬 Entertainment'),
    ]

    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-start-3 small border-dark',
            'placeholder': 'Search topics...'
        })
    )

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-pill border-dark fw-semibold',
            'onchange': 'this.form.submit();'
        })
    )