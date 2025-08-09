from django import forms
from .models import Article
from django.contrib.auth import get_user_model


class ArticleForm(forms.ModelForm):
    author_choice = forms.ChoiceField(
        label="Или выберите из ваших данных",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mt-2'})
    )

    class Meta:
        model = Article
        fields = ['title', 'author', 'content', 'preview', 'publication_status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Настраиваем поле author
        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя автора'
        })

        # Заполняем варианты выбора для текущего пользователя
        user = self.request.user
        choices = [
            ('', '--- Выберите вариант ---'),
            (user.username, f"Мой юзернейм: {user.username}"),
        ]
        if user.get_full_name():
            choices.append((user.get_full_name(), f"Моё имя: {user.get_full_name()}"))

        self.fields['author_choice'].choices = choices

        # Скрываем статус публикации если нет прав
        if not self.request.user.has_perm('blog.can_publish_article'):
            self.fields['publication_status'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        # Если выбран вариант из списка, используем его
        if cleaned_data.get('author_choice'):
            cleaned_data['author'] = cleaned_data['author_choice']
        return cleaned_data