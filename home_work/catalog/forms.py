from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Product, Category


class ProductForm(ModelForm):
    # Список запрещённых слов
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image']
        # fields = "__all__"
#
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["price"].required = True
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["image"].widget.attrs.update(
            {"accept": "image/jpeg, image/png", "class": "form-control-file"}
        )
        self.fields["description"].widget.attrs.update({"rows": 4})

    def clean_name(self):
        """Проверка названия на запрещённые слова"""
        name = self.cleaned_data.get("name", "")
        if name:
            lower_name = name.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in lower_name:
                    raise ValidationError(
                        f'Название содержит запрещённое слово: "{word}"!',
                        code="forbidden_word_in_name",
                    )
        return name

    def clean_description(self):
        """Проверка описания на запрещённые слова"""
        description = self.cleaned_data.get("description", "")
        if description:
            lower_desc = description.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in lower_desc:
                    raise ValidationError(
                        f'Описание содержит запрещённое слово: "{word}"!',
                        code="forbidden_word_in_description",
                    )
        return description

    def clean_price(self):
        """Проверка цены"""
        price = self.cleaned_data.get("price")
        if price is None:
            raise ValidationError("Укажите цену продукта!")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной!")
        return price

    def clean_image(self):
        """Проверка изображения"""
        image = self.cleaned_data.get("image")
        if image:

            if not image.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError("Допустимы только JPG/JPEG/PNG файлы!")

            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Максимальный размер файла - 5MB!")
        return image


class ProductModeratorForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'publication_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["image"].widget.attrs.update(
            {"accept": "image/jpeg, image/png", "class": "form-control-file"}
        )
        self.fields["description"].widget.attrs.update({"rows": 4})