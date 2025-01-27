<template>
  <svg xmlns="http://www.w3.org/2000/svg" style="display: none">
    <symbol id="search-icon" fill="currentColor" viewBox="0 0 16 16">
      <path
        d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"
      />
    </symbol>
  </svg>

  <div class="position-relative" ref="container" @click="handleFocused">
    <input
      class="header__search-input form-control fs-6 bg-dark-light border-0"
      :style="inputTextStyle"
      type="text"
      placeholder="Поиск"
      @input="handleInput"
      v-model="inputText"
      ref="inputComponent"
    />
    <div v-if="isExpanded" class="suggestions">
      <p class="text-start">
        Используйте ключевые фразы для эффективного поиска:
      </p>
      <hr />
      <button
        class="suggestions__button d-block rounded-3 mb-2"
        @click="applyFilterSearch"
        id="tag-search"
      >
        <svg class="me-3" role="img" width="16" height="16">
          <use xlink:href="#search-icon" />
        </svg>
        <span>Искать по тегу:[тег]</span>
      </button>
      <button
        class="suggestions__button d-block rounded-3 mb-2"
        @click="applyFilterSearch"
        id="category-search"
      >
        <svg class="me-3" role="img" width="16" height="16">
          <use xlink:href="#search-icon" />
        </svg>
        <span>Искать по категории:[категория]</span>
      </button>
      <button
        class="suggestions__button d-block rounded-3 mb-2"
        @click="applyFilterSearch"
        id="collection-search"
      >
        <svg class="me-3" role="img" width="16" height="16">
          <use xlink:href="#search-icon" />
        </svg>
        <span>Искать по коллекции:[коллекция]</span>
      </button>
      <button
        class="suggestions__button d-block rounded-3 mb-2"
        @click="applyFilterSearch"
        id="title-search"
      >
        <svg class="me-3" role="img" width="16" height="16">
          <use xlink:href="#search-icon" />
        </svg>
        <span>Искать по заголовку:[название заголовка]</span>
      </button>
      <button
        class="suggestions__button d-block rounded-3 mb-2"
        @click="applyFilterSearch"
        id="author-search"
      >
        <svg class="me-3" role="img" width="16" height="16">
          <use xlink:href="#search-icon" />
        </svg>
        <span>Искать по автору поста:[имя пользователя]</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type SearchModel from "@/models/SearchModel";
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";

const KEYWORDS = {
  "тег:": "tag",
  "категория:": "category",
  "коллекция:": "collection",
  "автор:": "author",
  "заголовок:": "title",
};
const BASE_COLOR = "#F2F2F2 !important";
const KEYWORD_COLOR = "#ADF0FF !important";

const store = useStore();

const inputText = ref("");
const isExpanded = ref(false);
const inputTextStyle = ref({ color: BASE_COLOR });
const inputComponent = ref<HTMLElement>();
const container = ref<HTMLElement>();
const searchInput = computed<SearchModel>(
  () => store.state.search.searchInput
);

const handleInput = () => {
  let inputKeyword = "";
  if (inputText.value.includes(":")) {
    inputKeyword = `${inputText.value.toLowerCase().split(":")[0]}:`;
  }

  if (!Object.keys(KEYWORDS).includes(inputKeyword)) {
    store.dispatch("search/updateSearchInput", {
      query: inputText.value,
      method: "full",
    });
  } else {
    const inputTextLower = inputText.value.toLowerCase();
    for (const [keyword, method] of Object.entries(KEYWORDS)) {
      if (inputTextLower.startsWith(keyword)) {
        inputKeyword = keyword;
        store.dispatch("search/updateSearchInput", {
          query: inputText.value.substring(keyword.length).trim(),
          method: method,
        });
        break;
      }
    }
  }

  highlightKeywords(inputKeyword);
};

const handleChangeSearchInput = () => {
  let searchKeyword = "";

  if (searchInput.value.method === "full") {
    inputText.value = searchInput.value.query;
  } else {
    for (const [keyword, method] of Object.entries(KEYWORDS)) {
      if (searchInput.value.method === method) {
        inputText.value = `${keyword}${searchInput.value.query}`;
        searchKeyword = keyword;
        break;
      }
    }
  }

  highlightKeywords(searchKeyword);
  isExpanded.value = false;
  store.commit("search/setSuggestionsOpen", false);
};

const highlightKeywords = (keyword: string) => {
  if (!Object.keys(KEYWORDS).includes(keyword)) {
    inputTextStyle.value.color = BASE_COLOR;
  } else {
    inputTextStyle.value.color = KEYWORD_COLOR;
  }
};

const applyFilterSearch = (event: MouseEvent) => {
  const buttonId = (event.currentTarget as HTMLElement).id;
  for (const [keyword, method] of Object.entries(KEYWORDS)) {
    if (buttonId.startsWith(method)) {
      inputText.value = keyword;
      break;
    }
  }

  isExpanded.value = false;
  store.commit("search/setSuggestionsOpen", false);
};

const handleFocused = () => {
  isExpanded.value = true;
  inputComponent.value?.focus();
  store.commit("search/setSuggestionsOpen", true);
};

const handleClickOutside = (event: MouseEvent) => {
  if (container.value && !container.value.contains(event.target as Node)) {
    isExpanded.value = false;
    store.commit("search/setSuggestionsOpen", false);
  }
};

watch(inputText, () => {
  if (inputText.value) {
    isExpanded.value = false;
    store.commit("search/setSuggestionsOpen", false);
  } else {
    isExpanded.value = true;
    store.commit("search/setSuggestionsOpen", true);
  }
});

watch(searchInput.value, () => {
  handleChangeSearchInput();
});

onMounted(() => {
  document.addEventListener("mousedown", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("mousedown", handleClickOutside);
});
</script>

<style scoped>
.header__search-input {
  border: 1px solid var(--secondary-light) !important;
  border-radius: 0.4em !important;
  box-shadow: none !important;
}

.header__search-input:focus {
  color: var(--light) !important;
  background-color: var(--dark-light) !important;
  outline: var(--primary) solid 1px !important;
}

input[type="search"]::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}

.suggestions {
  background-color: var(--dark-light);
  border: 1px solid var(--primary);
  border-radius: 0.4em !important;
  padding: 10px;
  margin-top: 5px;
  position: absolute !important;
  z-index: 1;
  width: 100%;
  left: 0;
}

.suggestions__button {
  border: 1px solid var(--secondary) !important;
  border-radius: 0.4em !important;
  color: var(--text-color);
  background-color: var(--secondary);
  font-weight: 400;
  line-height: 1.5;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.suggestions__button:hover {
  background-color: var(--dark-light);
}

@media only screen and (min-width: 200px) and (max-width: 768px) {
  .suggestions {
    display: none !important;
  }
}
</style>
