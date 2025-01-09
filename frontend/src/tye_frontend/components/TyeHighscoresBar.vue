<template>
  <div class="highscores-bar">
    <div class="highscores-bar__title">
      <h2 class="highscores-bar__title-text">HIGH SCORES</h2>
    </div>
    <div class="highscores-bar__container">
      <div class="highscores-bar__header-container">
        <div class="highscores-bar__header">
          <div class="rank">#</div>
          <div class="name">NAME</div>
          <div class="score">SCORE</div>
        </div>
        <div class="highscores-bar__list-container">
          <div class="highscores-bar__list">
            <div
              v-for="(score, index) in scores"
              :key="index"
              class="highscores-bar__list-item"
            >
              <div class="highscores-bar__list-item__content">
                <span class="rank">{{ index + 1 }}</span>
                <span class="name">{{ score.username }}</span>
                <span class="score">{{ score.highScore }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="highscores-bar__footer">
          <a
            href="https://github.com/teenxsky/tye/releases/tag/0.0.1"
            target="_blank"
          >
            PLAY NOW
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
// import HighscoreDataService from "@/services/HighscoreDataService";
// import type HighscoreModel from "@/models/HighscoreModel";

// const scores = ref<HighscoreModel[]>([]);
const scores = ref([
  { username: "Player1", highScore: 100 },
  { username: "Player2", highScore: 90 },
  { username: "Player3", highScore: 80 },
  { username: "Player4", highScore: 70 },
  { username: "Player5", highScore: 60 },
]);
</script>

<style scoped>
@font-face {
  font-family: "Press Start 2P";
  font-style: normal;
  src: url("@/tye_frontend/assets/fonts/PressStart2P.ttf") format("truetype");
}

.highscores-bar {
  background-image: url("@/tye_frontend/assets/images/background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 0.4rem !important;
  padding: 1rem;
}

.highscores-bar__title-text,
.highscores-bar__list-item__content {
  color: white;
  text-shadow: rgb(50, 90, 230) 3px 3px 0;
  margin: 0;
  font-size: large;
  font-family: "Press Start 2P", sans-serif;
}

.highscores-bar__title-text {
  margin-bottom: 1rem;
}

.highscores-bar__header {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr;
  margin-bottom: 0.5rem;
}

.highscores-bar__header,
.highscores-bar__footer a {
  color: rgb(240, 230, 20);
  text-shadow: rgb(250, 0, 10) 3px 3px 0;
  font-family: "Press Start 2P", sans-serif;
}

.highscores-bar__list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.highscores-bar__list-item__content {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr;
}

.highscores-bar__footer {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
</style>
