<template>
  <div v-if="!loading" class="profile-edit px-5">
    <div class="profile-edit container-fluid p-0">
      <div class="profile-edit__content row">
        <div class="profile-edit__content__left col-md-3">
          <div
            class="profile-edit__avatar-container d-flex flex-column gap-3 p-3 align-items-center"
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
                    Ваше имя (Необязательное поле)
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
                    Ваша фамилия (Необязательное поле)
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
                    Ваше отчество (Необязательное поле)
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
                <div class="d-flex align-items-center gap-2">
                  <button
                    type="submit"
                    class="btn btn-submit text-decoration-none"
                    :class="{
                      'action-checked': canSave,
                      'action-unchecked': !canSave,
                    }"
                    :disabled="!canSave || loadingUpdate"
                  >
                    <span v-if="!loadingUpdate"> Сохранить </span>
                    <LoadingCircle v-else class="spinner-border-sm" />
                  </button>
                  <p class="text-alert fs-7 m-0">{{ errorMessage }}</p>
                </div>
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

  <LoadingCircle v-else class="mx-auto my-auto" />
</template>

<script lang="ts" setup>
import _ from "lodash";
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import ProfileDataService from "@/services/ProfileDataService";
import UniversityModel from "@/models/UniversityModel";
import MajorModel from "@/models/MajorModel";
import type { ProfileDetailModel } from "@/models/ProfileModel";
import LoadingCircle from "@/components/LoadingCircle.vue";
import router from "@/router";

const store = useStore();
const loading = ref(true);
const loadingUpdate = ref(false);
const errorMessage = ref("");
const profile = ref<ProfileDetailModel>({
  ...store.getters["profile/getDefaultProfile"],
});
const profileEdit = ref<ProfileDetailModel>({ ...profile.value });
const avatar = ref<File | null>(null);
const universities = computed<UniversityModel[]>(
  () => store.getters["registry/getUniversities"]
);
const majors = computed<MajorModel[]>(
  () => store.getters["registry/getMajors"]
);

const canSave = computed(() => {
  return !_.isEqual(profile.value, profileEdit.value);
});

function isError() {
  return errorMessage.value !== "";
}

function clearError() {
  errorMessage.value = "";
}

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
  loadingUpdate.value = true;

  clearError();

  const profileEditData = { ...profileEdit.value };
  delete profileEditData.avatar;

  await Promise.all([
    avatar.value
      ? ProfileDataService.updateAvatar(avatar.value)
      : Promise.resolve(),
    ProfileDataService.updateProfile(profileEditData),
  ]).catch((error) => {
    console.error(error);
    if (error.data && typeof error.data === "object") {
      for (const key in error.data) {
        if (Object.prototype.hasOwnProperty.call(error.data, key)) {
          errorMessage.value = `${error.data[key].join(", ")}`;
          break;
        }
      }
    } else {
      errorMessage.value = error.data;
    }
  });

  if (isError()) {
    loadingUpdate.value = false;
    return;
  }

  await store
    .dispatch("profile/fetchProfile")
    .then(() => {
      router.push({
        name: "profile",
        params: { username: store.getters["profile/getProfile"].username },
      });
    })
    .catch((error) => {
      errorMessage.value = error.data.detail || error.data.message;
    })
    .finally(() => {
      loadingUpdate.value = false;
    });
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
    avatar.value = file;
  }
};
</script>

<style scoped>
.profile-edit__field-label {
  text-align: left;
  font-size: 1rem;
  text-decoration: underline;
  text-decoration-color: var(--primary);
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
  background-color: var(--secondary);
  color: var(--light);
  padding: 0.2rem 0.25rem;
  border: 0;
  border-radius: 0.4rem;
}

.form-control:focus,
.form-control:active {
  background-color: var(--secondary);
  color: var(--light);
  box-shadow: 0 0 0 0.25rem var(--primary);
}

.form-control:disabled,
.form-control:read-only {
  background-color: var(--secondary);
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
  object-fit: cover;
  width: 100%;
  height: auto;
  aspect-ratio: 1 / 1;
}

.btn-submit {
  width: 8rem;
  text-align: center;
}
</style>
