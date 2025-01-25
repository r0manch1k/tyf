<template>
  <div v-if="!loading" class="h-100 p-4">
    <div
      class="card rounded-0 border-top-0 border-bottom-0 bg-dark-light border-light p-4"
      style="border-left: 0 !important; border-right: 0 !important"
    >
      <div class="row flex-md-row">
        <div class="mb-3 mb-md-0 flex-shrink-0">
          <div class="d-flex align-items-center gap-2">
            <router-link :to="'/profile/' + post!.author.username">
              <img
                :src="post!.author.avatar"
                alt="avatar"
                class="img-fluid rounded-circle"
                style="width: 50px; height: 50px"
              />
            </router-link>
            <div class="d-flex flex-column">
              <router-link
                :to="'/profile/' + post!.author.username"
                class="text-light fs-6 mb-1"
              >
                {{ post!.author.username }}
              </router-link>
              <span class="fs-9 text-muted">
                <i class="bi bi-calendar3 me-1"></i>{{ post!.created_at }}
              </span>
            </div>
          </div>
          <hr />
        </div>
        <!--TODO: why we use props here instead post.ide...-->
        <AddCommentFormVue :postId="props!.identifier" :profile="profile" />
        <div class="post-info d-flex gap-3 text-muted">
          <span class="fs-9">
            <a href="#" class="text-muted fs-9">
              <i class="bi bi-collection me-1"></i>{{ post!.category.name }}
            </a>
          </span>
          <span class="fs-9">
            <a href="#attachments" class="text-muted fs-9">
              <i class="bi bi-paperclip"></i>{{ post!.media.length }}
              files
            </a>
          </span>
        </div>
        <div>
          <h1 class="fs-3 text-light text-start">{{ post!.title }}</h1>
          <div
            class="post-description rounded bg-dark-subtle text-light fs-6 mt-4 text-start"
            v-html="renderedContent"
          ></div>
        </div>
      </div>
      <h3 class="mb-4 fs-3 text-start text-light">Comments</h3>
      <CommentsList :comments="nestedComments" />
    </div>
  </div>
  <LoadingCircle v-else />
</template>

<script setup lang="ts">
import CommentsList from "@/components/CommentsList.vue";
import LoadingCircle from "@/components/LoadingCircle.vue";
import AddCommentFormVue from "@/components/AddCommentForm.vue";
import type CommentModel from "@/models/CommentModel";
import type { PostDetailModel } from "@/models/PostModel";
import PostDataService from "@/services/PostDataService";
import { ProfileDetailModel } from "@/models/ProfileModel";
import { useStore } from "vuex";
import { marked } from "marked";
import { onMounted, ref, defineProps } from "vue";

const props = defineProps({
  identifier: String,
});

const store = useStore();
const post = ref<PostDetailModel | null>(null);
const loading = ref(true);
const renderedContent = ref<string>("");
const nestedComments = ref<CommentModel[]>([]);
const profile = ref<ProfileDetailModel>({
  ...store.getters["profile/getDefaultProfile"],
});

// rewrite this
// onMounted(async () => {
//   if (props.identifier) {
//     post.value = await PostDataService.getPostByIdentifier(props.identifier);
//   } else {
//     console.error("Identifier is undefined");
//   }
//
//   if (post.value?.content) {
//     const markdown = await marked(post.value.content);
//     renderedContent.value = markdown;
//   } else {
//     renderedContent.value = "";
//   }
//
//   if (post.value?.comments) {
//     nestedComments.value = post.value.comments;
//   }
//   loading.value = false;
// });

onMounted(async () => {
  loading.value = true;

  if (props.identifier) {
    post.value = await PostDataService.getPostByIdentifier(props.identifier);
  } else {
    console.error("Identifier is undefined");
  }

  if (post.value?.content) {
    const markdown = await marked(post.value.content);
    renderedContent.value = markdown;
  } else {
    renderedContent.value = "";
  }

  if (post.value?.comments) {
    nestedComments.value = post.value.comments;
  }

  await Promise.all([
    store.dispatch("profile/fetchProfile").then(() => {
      profile.value = store.getters["profile/getProfile"];
    }),
  ]).finally(() => {
    loading.value = false;
  })
});
</script>

<style>
.comments-form textarea {
  height: 200px;
  background-color: #1d1d1d;
}

.comments-form textarea:focus {
  background-color: #1d1d1d !important;
}
</style>
