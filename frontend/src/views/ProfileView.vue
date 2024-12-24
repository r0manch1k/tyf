<template>
  <div v-if="!loading">
    <h1>{{ profile.username }}</h1>
    <p>{{ profile.bio }}</p>
  </div>
  <div v-else>
    <LoadingCircle />
  </div>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import { ref, defineProps, onMounted, computed } from "vue";
import { useStore } from "vuex";

const loading = ref(true);

const props = defineProps({
  username: String,
});

const store = useStore();

const profile = computed(() => {
  return store.getters["profile/getProfileByUsername"](props.username);
});

onMounted(async () => {
  await store.dispatch("profile/fetchProfileByUsername", props.username);
  loading.value = false;
});
</script>
