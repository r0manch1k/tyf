<template>
  <input
    type="email"
    class="form-control form-control-sm"
    style="border-radius: 0.4rem"
    id="email"
    placeholder="name@example.com"
    required
    aria-invalid="true"
    v-model="localEmail"
    @input="$emit('update:modelValue', localEmail)"
  />
  <label for="id_email"
    >Адрес эл. почты <span style="color: rgb(188, 28, 28)">*</span></label
  >
</template>

<script setup>
import { ref, defineProps } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
});

const localEmail = ref(props.modelValue);
</script>
