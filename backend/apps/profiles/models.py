from functools import partial

# Do not remove PIL
# from PIL import Image
import requests
from django.core.files.base import ContentFile
from django.db import models
from rest_framework import status
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from random_username.generate import generate_username
from apps.registry.models import Major, University
from apps.utils.media_tools import generate_media_path
from tyf import settings


validator_telegram = RegexValidator(
    regex=r"^(?:|(https?:\/\/)?(|www)[.]?((t|telegram)\.me)\/)[a-zA-Z0-9_]{5,32}$",
    message="Telegram profile link should be in the format of https://t.me/username or https://telegram.me/username",
)

validator_vkontakte = RegexValidator(
    regex=r"^(?:|(https?:\/\/)?(|www)[.]?(vk\.com)\/)[a-zA-Z0-9_]{3,32}$",
    message="VK profile link should be in the format of https://vk.com/username",
)

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        blank=False,
        null=True,
        related_name="profile",
    )
    email = models.EmailField(unique=False, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="University",
    )
    major = models.ForeignKey(
        Major,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Major",
    )
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = ResizedImageField(
        crop=["middle", "center"],
        size=[350, 350],
        force_format="WEBP",
        quality=100,
        upload_to=partial(generate_media_path, key="email", remove_with_same_key=True),
        blank=True,
        null=False,
        verbose_name="Avatar",
    )
    thumbnail = models.ImageField(
        upload_to=partial(generate_media_path, key="email", remove_with_same_key=True),
        blank=True,
        null=True,
        verbose_name="Thumbnail",
    )
    points = models.IntegerField(default=0, blank=True, null=True)
    awards = models.IntegerField(default=0, blank=True, null=True)
    telegram = models.URLField(
        blank=True, null=True, validators=[validator_telegram], verbose_name="Telegram"
    )
    vkontakte = models.URLField(
        blank=True, null=True, validators=[validator_vkontakte], verbose_name="VK"
    )
    __original_mode = None

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):
        # if self.avatar != self.__original_mode:
        #     self.__original_mode = self.avatar
        #     self.save_thumbnail()

        if not self.username:
            username = generate_username()[0]
            while Profile.objects.filter(username=username).exists():
                username = generate_username()[0]
            self.username = generate_username()[0]

        super(Profile, self).save(force_insert, force_update, *args, **kwargs)

    # def save_thumbnail(self):
    #     if not self.avatar:
    #         return
    #     image = Image.open(self.avatar)
    #     image.thumbnail((49, 50), Image.Resampling.LANCZOS)
    #     thumb_name, _ = os.path.splitext(self.avatar.name)
    #     thumb_filename = thumb_name + "_thumb" + ".webp"
    #     image.save(MEDIA_ROOT + thumb_filename, "WEBP")
    #     self.thumbnail = thumb_filename
    #     return True

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def is_following(self, profile):
        return self.following.filter(following_id=profile.id).exists()

    def is_followed(self, profile):
        return self.followers.filter(follower_id=profile.id).exists()

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return settings.DEFAULT_USER_AVATAR

    @property
    def get_telegram(self):
        if self.telegram:
            return "@" + self.telegram.split("/")[-1]
        return None

    @property
    def get_vkontakte(self):
        if self.vkontakte:
            return self.vkontakte.split("/")[-1]
        return None

    def save_avatar_from_url(self, url):
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            filename = "avatar"
            self.avatar.save(filename, ContentFile(response.content), save=False)

    def __str__(self):
        return self.username
