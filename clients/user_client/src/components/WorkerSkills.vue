<template>
  <div class="box; border_main1">
    <div v-if="skills" style="overflow:hidden">
      <p class="bold">
        Выбрать услуги для сотрудника
      </p>
      <li v-for="skill in skills" :key="skill.service.service_id">
        <input type="checkbox" id="String(skill.service.service_id)" :value=skill.picked v-model="skill.picked" />
        <label :for="String(skill.service.service_id)" >{{ skill.service.name }}</label>
      </li>
      <button
        style="float: right"
        @click="updateSkills"
      >
        Сохранить
      </button>
    </div>
    <div v-if="!skills">
      <p class="bold">Нет услуг для выбора </p>
      <p class="bold">
        <router-link to="services">
          <a> 
            Перейти к услугам
          </a>
        </router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { DefaultService, type SkillIn, type SkillOut } from "@/client";

declare interface Data {
  skills: SkillOut[];
}

export default {
  components: {},
  computed: {
    updatedSkills(): SkillIn[] {
      const updatedSkills: SkillIn[] = this.skills.map(s => { 
        return {
          picked: s.picked,
          worker_id: parseInt(this.worker_id),
          service_id: s.service.service_id,
        }
      })
      return updatedSkills
    }
  },
  data(): Data {
    return {
      skills: [],
    };
  },
  methods: {
    async fetchSkills() {
      this.skills = (
        await DefaultService.getSkills(undefined, parseInt(this.worker_id))
      ).skills;
    },
    async updateSkills() {
      await DefaultService.addSkills({skills: this.updatedSkills})
      this.skills = [];
      await this.fetchSkills();
    }
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
