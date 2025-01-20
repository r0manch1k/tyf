<template>
  <div class="post-create">
    <div class="post-create__header">
      <h1 class="post-create__header__title">Создание поста</h1>
    </div>
    <div class="post-create__body">
      <form class="post-create__body__form" @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="title" class="form-label">Заголовок</label>
          <input
            type="text"
            class="form-control"
            id="title"
            v-model="post.title"
            placeholder="Введите заголовок"
          />
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Описание</label>
          <textarea
            class="form-control"
            id="description"
            v-model="post.description"
            rows="3"
            placeholder="Введите описание"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Контент</label>
          <textarea
            class="form-control"
            id="content"
            v-model="post.content"
            rows="3"
            placeholder="Введите контент"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="media" class="form-label">Файл</label>
          <input
            class="form-control"
            type="media"
            id="media"
            @change="handlemediaUpload"
          />
        </div>
        <button type="submit" class="btn btn-primary">Создать</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import type PostModel from "@/models/PostModel";
import PostDataService from "@/services/PostDataService";
import { ref } from "vue";

const post = ref<PostModel>(PostDataService.getNewPost());

const media = ref<File | null>(null);

const handlemediaUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    media.value = target.files[0];
  }
};

const submitForm = async () => {
  try {
    const formData = new FormData();
    formData.append("title", post.value.title);
    formData.append("description", post.value.description);
    formData.append("content", post.value.content);
    if (media.value) {
      formData.append("media", media.value);
    }
    const newPost: PostModel = {
      ...post.value,
      media: media.value ? [media.value.name] : [],
    };
    await PostDataService.createPost(newPost);
    alert("Пост успешно создан!");
  } catch (error) {
    console.error("Ошибка при создании поста:", error);
  }
};
</script>
