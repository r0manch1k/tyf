<template>
  <form id="edit-form" class="d-none mt-4">
    <fieldset>
      <div class="mb-3">
        <label for="edit-comment" class="form-label">Edit Comment</label>
        <textarea
          id="edit-comment"
          class="form-control"
          rows="3"
          placeholder="Edit your comment..."
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <button type="button" class="btn btn-secondary cancel-edit">
        Cancel
      </button>
    </fieldset>
  </form>
</template>

<style></style>

<script setup lang="ts"></script>
