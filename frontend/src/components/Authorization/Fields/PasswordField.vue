<template>
  <input
    type="password"
    name="password"
    class="form-control form-control-sm"
    style="border-radius: 1rem"
    id="id_password"
    placeholder="Password"
    required
    aria-invalid="true"
    v-model="localPassword"
    @input="$emit('update:modelValue', localPassword)"
  />
  <label for="id_password"
    >Пароль <label style="color: rgb(188, 28, 28)">*</label></label
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

const localPassword = ref(props.modelValue);
</script>
