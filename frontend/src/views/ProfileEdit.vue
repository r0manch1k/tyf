<template>
  <div class="profile-edit">
    <div class="profile-edit__header">
      <h1>Edit Profile</h1>
    </div>
    <div class="profile-edit__content">
      <div class="profile-edit__content__left">
        <div class="profile-edit__content__left__avatar">
          <img src="https://via.placeholder.com/150" alt="Avatar" />
        </div>
        <div class="profile-edit__content__left__username">
          <h2>Username</h2>
          <p>username</p>
        </div>
        <div class="profile-edit__content__left__email">
          <h2>Email</h2>
          <p>email</p>
        </div>
        <div class="profile-edit__content__left__bio">
          <h2>Bio</h2>
          <p>bio</p>
        </div>
      </div>
      <div class="profile-edit__content__right">
        <div class="profile-edit__content__right__form">
          <form>
            <div class="form-group">
              <label for="username">Username</label>
              <input type="text" id="username" name="username" />
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" />
            </div>
            <div class="form-group">
              <label for="bio">Bio</label>
              <textarea id="bio" name="bio"></textarea>
            </div>
            <button type="submit">Save</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup></script>
