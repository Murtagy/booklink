<template>
  <div class="box; border_main1">
    <div v-if="skills.length == 0 && loaded_skills">
      <p class="bold">Нет услуг для выбора</p>
        <router-link to="/services">
          <a> Перейти к услугам </a>
        </router-link>
    </div>
    <div v-else v-if="skills" style="overflow: hidden">
      <p class="bold">Реализуемые услуги</p>
      <li v-for="skill in skills" :key="skill.service.service_id">
        <input
          type="checkbox"
          id="String(skill.service.service_id)"
          :value="skill.picked"
          v-model="skill.picked"
        />
        <label :for="String(skill.service.service_id)">{{
          skill.service.name
        }}</label>
      </li>
      <button style="float: right" @click="updateSkills">Сохранить</button>
    </div>
  </div>
</template>

<script lang="ts">
import { DefaultService, type SkillIn, type SkillOut } from "@/client";

declare interface Data {
  skills: SkillOut[];
  loaded_skills: boolean;
}

export default {
  components: {},
  computed: {
    updatedSkills(): SkillIn[] {
      const updatedSkills: SkillIn[] = this.skills.map((s) => {
        return {
          picked: s.picked,
          worker_id: parseInt(this.worker_id),
          service_id: s.service.service_id,
        };
      });
      return updatedSkills;
    },
  },
  data(): Data {
    return {
      skills: [],
      loaded_skills: false,
    };
  },
  methods: {
    async fetchSkills() {
      this.skills = (
        await DefaultService.getSkills(undefined, parseInt(this.worker_id))
      ).skills;
      this.loaded_skills = true;
    },
    async updateSkills() {
      await DefaultService.addSkills({ skills: this.updatedSkills });
      this.skills = [];
      await this.fetchSkills();
    },
  },
  mounted() {
    this.fetchSkills();
  },
  props: {
    worker_id: {
      type: String,
      required: true,
    },
  },
};
</script>
