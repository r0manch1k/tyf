<template>
  <div class="highscores-bar">
    <div v-if="!loading">
      <!-- <h3 class="highscores-bar__title-header">
        <span class="highscores-bar__header-text">Tell Your Enemies</span>
        <span class="highscores-bar__emoji"> 🚀</span>
      </h3>
      <h4 class="highscores-bar__subtitle">
        Наш новый проект, в котором вы можете соревноваться с друзьями.
        <a
          class="highscores-bar__details"
          href="https://tellyourenemies.ru"
          target="_blank"
          >Подробнее...</a
        >
      </h4> -->
      <div class="highscores-bar__content">
        <div class="highscores-bar__title">
          <h2 class="highscores-bar__title-text">HIGH SCORES</h2>
        </div>
        <div class="highscores-bar__container">
          <div class="highscores-bar__header-container">
            <div class="highscores-bar__header">
              <div class="highscores-bar__rank">#</div>
              <div class="highscores-bar__name">NAME</div>
              <div class="highscores-bar__score">SCORE</div>
            </div>
            <div class="highscores-bar__list-container">
              <div class="highscores-bar__list">
                <div
                  v-for="(score, index) in scores"
                  :key="index"
                  class="highscores-bar__list-item"
                >
                  <div class="highscores-bar__list-item-content">
                    <span class="highscores-bar__rank">{{ index + 1 }}</span>
                    <span class="highscores-bar__name" :title="score.username">
                      {{
                        score.username.length > 10
                          ? score.username.substring(0, 10)
                          : score.username
                      }}
                    </span>
                    <span class="highscores-bar__score">{{
                      score.highScore
                    }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="highscores-bar__footer">
              <a
                href="https://github.com/teenxsky/tye/releases/tag/0.0.1"
                target="_blank"
                class="highscores-bar__footer-link"
              >
                WHAT IS THAT?
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <LoadingCircle class="spinner-border-sm mx-auto my-auto" v-else />
  </div>
</template>

<script setup lang="ts">
import LoadingCircle from "@/components/LoadingCircle.vue";
import type TyeUserModel from "@/tye_frontend/models/TyeUserModel";
import TyeDataService from "@/tye_frontend/services/TyeDataService";
import { onMounted, ref } from "vue";

const scores = ref<TyeUserModel[]>([
  { username: "Player1", highScore: 100 },
  { username: "Player2", highScore: 90 },
  { username: "Player3", highScore: 80 },
  { username: "Player4", highScore: 70 },
  { username: "Player5", highScore: 60 },
  { username: "Player6", highScore: 50 },
  { username: "Player7", highScore: 40 },
  { username: "Player8", highScore: 30 },
  { username: "Player9", highScore: 20 },
  { username: "Player10", highScore: 10 },
]);

const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  scores.value = await TyeDataService.getHighscores();
  loading.value = false;
});
</script>

<style scoped>
@font-face {
  font-family: "Press Start 2P";
  font-style: normal;
  src: url("@/tye_frontend/assets/fonts/PressStart2P.ttf") format("truetype");
}

/* .highscores-bar__content {
  margin-top: 1rem;
} */

.highscores-bar__header-text {
  color: rgb(240, 230, 20);
  text-decoration: underline;
  font-size: large;
  text-decoration-color: rgb(250, 0, 10) !important;
}

.highscores-bar {
  background-image: url("@/tye_frontend/assets/images/background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  text-align: center;
  border-radius: 0.4rem !important;
  padding: 1rem;
}

.highscores-bar__title-text,
.highscores-bar__list-item-content {
  color: white;
  text-shadow: rgb(50, 90, 230) 3px 3px 0;
  margin: 0;
  text-align: center;
  font-size: medium;
  font-family: "Press Start 2P", sans-serif;
}

.highscores-bar__subtitle {
  font-size: 1rem;
  color: #f8f9fa;
  /* text-align: left; */
  font-weight: normal;
}

.highscores-bar__details {
  font-size: 1rem;
  color: rgb(240, 230, 20);
  font-weight: normal;
  text-decoration: underline;
  text-decoration-color: rgb(240, 230, 20) !important;
}

.highscores-bar__title-header {
  font-size: 1rem;
  color: #f8f9fa;
  /* text-align: left; */
}

.highscores-bar__title-text {
  margin-bottom: 1rem;
}

.highscores-bar__header {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr;
  text-align: center;
  margin-bottom: 0.5rem;
}

.highscores-bar__header,
.highscores-bar__footer-link {
  color: rgb(240, 230, 20);
  text-shadow: rgb(250, 0, 10) 3px 3px 0;
  font-family: "Press Start 2P", sans-serif;
}

.highscores-bar__list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.highscores-bar__list-item-content {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr;
}

.highscores-bar__footer {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.highscores-bar__subtitle--p-2 {
  padding: 0.5rem;
}

.highscores-bar__subtitle--pt-1 {
  padding-top: 0.25rem;
}

.highscores-bar__subtitle--m-0 {
  margin: 0;
}

.highscores-bar__subtitle--fw-normal {
  font-weight: normal;
}

.highscores-bar__subtitle--text-start {
  text-align: left;
}
</style>
