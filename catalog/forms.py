from django import forms
from .models import Product


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
            return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
            return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")

            allowed_types = ['image/jpeg', 'image/png']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Неверный формат файла. Допускаются только JPEG и PNG.")

        return image
