<template>
  <div class="tablist">
    <ul class="nav nav-pills fs-7">
      <li class="nav-item">
        <button
          class="nav-link active"
          data-bs-toggle="pill"
          type="button"
          role="tab"
          aria-selected="true"
        >
          All
        </button>
      </li>
      <li v-for="tab in tablist" :key="tab.id" class="nav-item">
        <button
          class="nav-link"
          data-bs-toggle="pill"
          type="button"
          role="tab"
          aria-selected="true"
        >
          {{ tab.name }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, defineProps } from "vue";

const props = defineProps({
  tablist: Array,
});

onMounted(() => {
  console.log(props.tablist);
});
</script>

<style scoped>
.tablist {
  width: 100%;
}

ul {
  width: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.nav {
  flex-wrap: nowrap;
}

.nav-item {
  padding: 0.5rem 0.2rem !important;
  width: fit-content !important;
  border: 0 !important;
}

.nav-pills .nav-link.active {
  background-color: var(--primary);
  color: var(--dark);
}

.nav-pills .nav-link {
  white-space: nowrap;
  border-radius: 0.4rem;
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  background-color: var(--dark);
  color: var(--light);
}
</style>
