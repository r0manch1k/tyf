<template>
  <form id="reply-form" class="d-none mt-4">
    <fieldset>
      <div class="mb-3">
        <label for="reply-comment" class="form-label">Your Reply</label>
        <textarea
          id="reply-comment"
          class="form-control"
          rows="3"
          placeholder="Write a reply..."
        ></textarea>
      </div>
      <button
        type="submit"
        class="mb-2 btn border-start-0 border-top-0 btn-outline-primary mt-2 action-unchecked comments__reply"
      >
        Submit Reply
      </button>
    </fieldset>
  </form>
</template>

<style></style>

<script setup lang="ts"></script>
