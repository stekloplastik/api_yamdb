'''
from django.test import TestCase
from django.contrib.auth import get_user_model
Аноним — может просматривать описания, читать отзывы и комментарии.
Аутентифицированный пользователь (user)— может читать всё, как и Аноним,
дополнительно может публиковать отзывы и ставить рейтинг произведениям
(фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить оценки;
может редактировать и удалять свои отзывы и комментарии.
Модератор (moderator) — те же права, что и у Аутентифицированного пользователя
плюс право удалять и редактировать любые отзывы и комментарии.
Администратор (admin) — полные права на управление проектом и всем содержимым.
Может создавать и удалять произведения, категории и жанры.
Может назначать роли пользователям.
Администратор Django — те же права, что и у роли Администратор.
id,username,email,role,description,first_name,last_name
class UsersManagersTests(TestCase):
    #Создание Модератора/Пользователя
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = 'Valerka', email='normal@user.com', password='13',
            first_name = 'Valeriy', last_name = 'M'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.first_name, 'Valeriy')
        self.assertEqual(user.last_name, 'M')
        self.assertEqual(user.username, 'Valerka')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        try:
            self.assertFalse(user.is_superuser)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='',
                                     password="13", username = 'Valerka')
    #Создание Админа/АдминаДжанго
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username = 'Админ', email='super@user.com', password='13',
            first_name = 'Админ', last_name = 'A')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.first_name, 'Админ')
        self.assertEqual(admin_user.last_name, 'A')
        self.assertEqual(admin_user.username, 'Админ')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        try:
            self.assertTrue(admin_user.is_superuser)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username = 'Админ', email='super@user.com',
                password='123', is_superuser=False
            )
    #Для "Гостя" аналогичные тесты не корректны
'''