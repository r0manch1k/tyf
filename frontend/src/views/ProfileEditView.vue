<template>
  <div v-if="!loading" class="profile-edit px-5">
    <div class="profile-edit container-fluid p-0">
      <div class="profile-edit__content row">
        <div class="profile-edit__content__left col-md-3">
          <div
            class="profile-edit__avatar-container d-flex flex-column gap-3 p-3"
          >
            <img
              :src="profileEdit.avatar"
              alt="avatar"
              class="profile-edit__avatar img-fluid rounded-circle"
            />
          </div>
          <div class="profile-view__actions d-flex flex-column w-100 gap-2">
            <input
              type="file"
              accept="image/*"
              @change="onImageInput"
              :ref="profileEdit.avatar"
              multiple="false"
            />
            <button
              class="btn btn-action text-decoration-none text-light"
              @click="onImageClick"
            >
              Выбрать фото
            </button>
          </div>
        </div>
        <div class="profile-edit__content__right col-md-9 pt-3">
          <div
            class="profile-edit__content__right__form container-fluid text-start"
          >
            <form
              @submit.prevent="updateProfile"
              class="profile-edit__form row"
            >
              <div class="col-md-5">
                <div class="form-group mb-3">
                  <label for="username" class="profile-edit__field-label"
                    >Никнейм</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваш уникальный никнейм. Без пробелов
                  </p>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    class="form-control"
                    required
                    v-model.trim="profileEdit.username"
                    :placeholder="profile.username"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="first_nawme" class="profile-edit__field-label"
                    >Имя</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваше настоящее имя (Необязательное поле)
                  </p>
                  <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    class="form-control"
                    v-model.trim="profileEdit.first_name"
                    :placeholder="profile.first_name"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="last_name" class="profile-edit__field-label"
                    >Фамилия</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваша настоящая фамилия (Необязательное поле)
                  </p>
                  <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    class="form-control"
                    v-model.trim="profileEdit.last_name"
                    :placeholder="profile.last_name"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="middle_name" class="profile-edit__field-label"
                    >Отчество</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваше настоящее отчество (Необязательное поле)
                  </p>
                  <input
                    type="text"
                    id="middle_name"
                    name="middle_name"
                    class="form-control"
                    v-model.trim="profileEdit.middle_name"
                    :placeholder="profile.middle_name"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="bio" class="profile-edit__field-label">Bio</label>
                  <p class="profile-edit__field-sublabel">
                    Описание вашего профиля. Максимум 200 символов
                    (Необязательное поле)
                  </p>
                  <textarea
                    id="bio"
                    name="bio"
                    class="form-control"
                    v-model="profileEdit.bio"
                    :placeholder="profile.bio"
                  ></textarea>
                </div>
                <button type="submit" class="btn btn-submit">Сохранить</button>
              </div>
              <div class="col-md-5">
                <div class="form-group mb-3">
                  <label for="date_of_birth" class="profile-edit__field-label"
                    >Дата рождения</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваша дата рождения (Необязательное поле)
                  </p>
                  <input
                    type="date"
                    id="date_of_birth"
                    name="date_of_birth"
                    class="form-control"
                    v-model="profileEdit.date_of_birth"
                    :placeholder="profile.date_of_birth"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="university" class="profile-edit__field-label"
                    >Университет</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваш университет (Необязательное поле)
                  </p>
                  <select
                    id="university"
                    name="university"
                    class="form-control"
                    v-model="profileEdit.university"
                  >
                    <option
                      v-for="university in universities"
                      :key="university.id"
                      :value="university.id"
                    >
                      {{ university.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label for="major" class="profile-edit__field-label"
                    >Направление</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваше направление (Необязательное поле)
                  </p>
                  <select
                    id="major"
                    name="major"
                    class="form-control"
                    v-model="profileEdit.major"
                  >
                    <option
                      v-for="major in majors"
                      :key="major.id"
                      :value="major.id"
                    >
                      {{ major.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label for="telegram" class="profile-edit__field-label"
                    >Телеграм</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваша ссылка на Телеграм (Необязательное поле)
                  </p>
                  <input
                    type="text"
                    id="telegram"
                    name="telegram"
                    class="form-control"
                    v-model.trim="profileEdit.telegram"
                    :placeholder="profile.telegram"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="vkontakte" class="profile-edit__field-label"
                    >ВКонтакте</label
                  >
                  <p class="profile-edit__field-sublabel">
                    Ваша ссылка на ВКонтакте (Необязательное поле)
                  </p>
                  <input
                    type="text"
                    id="vkontakte"
                    name="vkontakte"
                    class="form-control"
                    v-model.trim="profileEdit.vkontakte"
                    :placeholder="profile.vkontakte"
                  />
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <LoadingCircle v-else />
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import ProfileDataService from "@/services/ProfileDataService";
import UniversityModel from "@/models/UniversityModel";
import MajorModel from "@/models/MajorModel";
import type { ProfileDetailModel } from "@/models/ProfileModel";
import LoadingCircle from "@/components/LoadingCircle.vue";

const store = useStore();
const loading = ref(true);
const profile = ref<ProfileDetailModel>({
  ...store.getters["profile/getDefaultProfile"],
});
const profileEdit = ref<ProfileDetailModel>({ ...profile.value });
const universities = computed<UniversityModel[]>(
  () => store.getters["registry/getUniversities"]
);
const majors = computed<MajorModel[]>(
  () => store.getters["registry/getMajors"]
);

onMounted(async () => {
  loading.value = true;
  await Promise.all([
    store
      .dispatch("profile/fetchProfile")
      .then(() => {
        profile.value = store.getters["profile/getProfile"];
        profileEdit.value = { ...profile.value };
      })
      .finally(() => {
        loading.value = false;
        console.log(profileEdit.value);
      }),
    store.getters["registry/getUniversities"]
      ? store.dispatch("registry/fetchUniversities")
      : Promise.resolve(),
    store.getters["registry/getMajors"]
      ? store.dispatch("registry/fetchMajors")
      : Promise.resolve(),
  ]).finally(() => {
    loading.value = false;
  });
});

const updateProfile = async () => {
  loading.value = true;
  console.log(profileEdit.value);
  for (const key in profileEdit.value) {
    const typedKey = key as keyof typeof profileEdit.value;
    if (profileEdit.value[typedKey] === null) {
      profileEdit.value[typedKey] = profile.value[typedKey];
    }
  }
  Promise.all([
    ProfileDataService.updateProfile(profileEdit.value),
    store.dispatch("profile/fetchProfile"),
  ]).finally(() => {
    loading.value = false;
  });

  loading.value = false;
};

const onImageClick = () => {
  const input = document.querySelector(
    "input[type='file']"
  ) as HTMLInputElement;
  if (input) {
    input.click();
  }
};

const onImageInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profileEdit.value.avatar = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};
</script>

<style scoped>
.profile-edit__field-label {
  text-align: left;
  font-size: 1rem;
}

.profile-edit__field-sublabel {
  text-align: left;

  font-size: smaller;
  color: var(--secondary-xx-light);
  margin: 0 0 0.25rem 0;
}

input[type="file"] {
  display: none;
}

.form-control {
  background-color: var(--dark-light);
  color: var(--light);
  padding: 0.2rem 0.25rem;
  border: 0;
  border-radius: 0.4rem;
}

.form-control:focus,
.form-control:active {
  background-color: var(--dark-light);
  color: var(--light);
  box-shadow: none;
}

.form-control:disabled,
.form-control:read-only {
  background-color: var(--dark-light);
}

input[type="date" i]::-webkit-inner-spin-button,
input[type="date" i]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  border-radius: 5px;
}

.profile-edit__avatar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: width;
  overflow: hidden;
}

.profile-edit__avatar {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
</style>
