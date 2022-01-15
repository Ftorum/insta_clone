from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
	picture = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

	class Meta:
		model = Post
		fields = ('picture', 'caption',)