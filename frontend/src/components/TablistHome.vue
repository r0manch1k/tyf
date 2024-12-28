<template>
  <div class="tablist-home">
    <ul class="nav nav-pills">
      <li v-for="category in categories" :key="category.id" class="nav-item">
        {{ category.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, defineProps } from "vue";

const props = defineProps({
  categories: Array,
});

onMounted(() => {
  // console.log(props.categories);
});
</script>
