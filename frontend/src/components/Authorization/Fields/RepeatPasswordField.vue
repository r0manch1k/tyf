<template>
  <input
    type="password"
    name="password2"
    class="form-control form-control-sm"
    style="border-radius: 0.4rem"
    id="id_password2"
    placeholder="Password confirmation"
    required
    aria-invalid="true"
    v-model="localRepeatPassword"
    @input="$emit('update:modelValue', localRepeatPassword)"
  />
  <label for="id_password2"
  >Повторите пароль <label style="color: rgb(188, 28, 28)">*</label></label
  >
</template>

<script setup>
import { defineProps, ref } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
});

const localRepeatPassword = ref(props.modelValue);
</script>
