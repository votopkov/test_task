from django import forms
from models import Comment, Product


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['product', 'name', 'comment']

    def clean_product(self):
        product_id = self.cleaned_data['product']

        product_object = Product.objects.get(id=product_id)

        return product_object

    product = forms.CharField()
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))
