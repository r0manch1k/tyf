<template>
  <div class="mt-5">
    <form>
      <fieldset>
        <div class="mb-3">
          <label for="create-comment" class="form-label">Your Comment</label>
          <textarea
            id="create-comment"
            class="form-control"
            rows="3"
            placeholder="Write a comment..."
          ></textarea>
        </div>
        <button
          class="mb-2 btn border-start-0 border-top-0 btn-outline-primary mt-0 fs-8 action-unchecked"
          type="submit"
        >
          Submit
        </button>
      </fieldset>
    </form>
  </div>
</template>

<style></style>

<script setup lang="ts"></script>
