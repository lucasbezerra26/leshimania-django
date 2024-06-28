from django import forms
from .models import MicroscopeSlide, MicroscopeImage, Laboratory


from django import forms
from dal import autocomplete
from .models import MicroscopeSlide, Laboratory


class MicroscopeSlideFormModal(forms.ModelForm):
    laboratory = forms.ModelChoiceField(
        queryset=Laboratory.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = MicroscopeSlide
        fields = ["slide_name", "laboratory"]
        widgets = {
            "slide_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user_filter = kwargs.pop("user_filter", None)
        super(MicroscopeSlideFormModal, self).__init__(*args, **kwargs)
        if user_filter:
            self.fields["laboratory"].queryset = Laboratory.objects.filter(
                participants=user_filter
            )


class MicroscopeImageForm(forms.ModelForm):
    class Meta:
        model = MicroscopeImage
        fields = ["image"]
        labels = {
            "image": "Imagem",
        }
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


# class MicroscopeImageForm(forms.ModelForm):
#     image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
#
#     class Meta:
#         model = MicroscopeImage
#         fields = ["image"]
#         labels = {
#             "image": "Imagem",
#         }
#         widgets = {
#             "image": forms.FileInput(attrs={"class": "form-control"}),
#         }
