<template>
  <div v-if="!loading" class="h-100 p-4">
    <div
      class="card rounded-0 border-top-0 border-bottom-0 bg-dark-light border-light p-4"
      style="border-left: 0 !important; border-right: 0 !important"
    >
      <h1 class="fs-3 text-light">Create New Post</h1>

      <form @submit.prevent="submitForm" class="mt-4">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input
            v-model="newPost.title"
            type="text"
            class="form-control"
            id="title"
            required
          />
        </div>

        <div class="mb-3">
          <label for="content" class="form-label">Content</label>
          <textarea
            v-model="newPost.content"
            class="form-control"
            id="content"
            rows="5"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea
            v-model="newPost.description"
            class="form-control"
            id="description"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="category" class="form-label">Category</label>
          <select
            v-model="newPost.category"
            class="form-select"
            id="category"
            required
          >
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label for="tags" class="form-label">Tags</label>
          <select v-model="newPost.tags" class="form-select" id="tags" multiple>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label for="thumbnail" class="form-label">Thumbnail</label>
          <input
            type="file"
            accept="image/*"
            @change="onImageInput"
            multiple="false"
          />
          <button
            type="button"
            class="btn btn-action text-decoration-none text-light"
            @click="onImageClick"
          >
            Выбрать изображение
          </button>
        </div>

        <button type="submit" class="btn btn-primary">Create Post</button>
      </form>
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import PostDataService from "@/services/PostDataService";
import { useStore } from "vuex";
import LoadingCircle from "@/components/LoadingCircle.vue";
import { ProfileDetailModel } from "@/models/ProfileModel";
import CategoryModel from "@/models/CategoryModel";
import CategoryDataService from "@/services/CategoryDataService";
import TagsDataService from "@/services/TagsDataService";
import TagModel from "@/models/TagModel";

const store = useStore();
const newPost = ref({
  title: "",
  content: "",
  description: "",
  category: "",
  tags: [] as string[],
  thumbnail: null as string | null,
});
const thumbnail = ref<File | null>(null);

const loading = ref(false);
const categories = ref<CategoryModel[]>([]);
const tags = ref<TagModel[]>([]);
const profile = ref<ProfileDetailModel>({
  ...store.getters["profile/getDefaultProfile"],
});

onMounted(async () => {
  loading.value = true;

  categories.value = await CategoryDataService.getAllCategories();
  tags.value = await TagsDataService.getAllTags();
  await store
    .dispatch("profile/fetchProfile")
    .then(() => {
      profile.value = store.getters["profile/getProfile"];
    })
    .finally(() => {
      loading.value = false;
    });
});

const onImageClick = () => {
  const input = document.querySelector(
    "input[type='file']"
  ) as HTMLInputElement;
  if (input) {
    input.click();
  }
};


const onImageInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    thumbnail.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      newPost.value.thumbnail = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const submitForm = async () => {
  loading.value = true;

  const formData = new FormData();
  formData.append("title", newPost.value.title);
  formData.append("content", newPost.value.content);
  formData.append("category", String(newPost.value.category));
  formData.append("description", newPost.value.description);

  if (newPost.value.tags) {
    newPost.value.tags.forEach((tagId: string) => {
      formData.append("tags[]", tagId);
    });
  }
  if (thumbnail.value) {
    formData.append("thumbnail", thumbnail.value as File);
  }
  console.log("thumbnail", formData.get("thumbnail"));

  try {
    const response = await PostDataService.createPost(formData);
    console.log("Post created successfully:", response);
  } catch (error) {
    console.error("Error creating post:", error);
  } finally {
    loading.value = false;
  }
};
</script>
