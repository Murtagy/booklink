<template>
  <div v-if="visit">
     <button
      v-if="!show_cancel"
      @click="show_cancel = !show_cancel"
      style="margin-top: 1em; margin-bottom: 1em; float: right"
      type="submit"
    >
      Удалить
    </button>
    <div v-if="show_cancel"> 
      <p class="bold">Вы уверены?</p>
      <input type="button" :value="cancelYes" @click="cancelVisit" />
      <input
        type="button"
        value="Нет, не отменять"
        @click="show_cancel = !show_cancel"
      />
    </div>
    <form @submit.prevent="updateVisit" class="border_main1">
      <p>
        Услуги:
        <span v-for="service of visit.services">
          {{ service.name }}
        </span>
      </p>
      <br>
      <p> 
        <p class="bold"> Данные о клиентe </p>
        <div id="client_data">
          Телефон - {{visit.visit.phone}}
          <br>
          Email - {{visit.visit.email}}
        </div>
      </p>
      <br>
      <label for="visit_from_time">Время начала визита </label>
      <input id="visit_from_time" type="time" v-model="from_time" required />
      <br>
      <label for="visit_to_time">Время конца визита </label>
      <input id="visit_to_time" type="time" v-model="to_time" required />
     <button class="save" type="submit">Сохранить</button>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutVisitExtended } from "@/client";
import { extended_visit_repr } from "@/extended_visit_repr";
import dayjs from "dayjs";

declare interface Data {
  show_cancel: boolean;
  from_time: string,
  to_time: string,
  visit?: OutVisitExtended;
}

export default {
  components: {},
  computed: {
    cancelYes(): string {
      if (!this.visit) {
        return "";
      }
      const visit_repr = extended_visit_repr(this.visit)
      return `Да, отменить визит, ${visit_repr}`;
    },
  },
  data(): Data {
    return {
      show_cancel: false,
      visit: undefined,
      from_time: '',
      to_time: '',
    };
  },
  methods: {
    async cancelVisit() {
      // TODO
    },
    async fetchVisit() {
      this.visit = await DefaultService.getVisitExtended(this.visit_id);
      this.from_time = dayjs(this.visit.visit.from_datetime).format('HH:mm')
      this.to_time = dayjs(this.visit.visit.to_datetime).format('HH:mm')
    },
    // async deleteVisit() {
    //   if (!this.visit) {
    //     return;
    //   }
    //   this.visit = undefined;
    //   await DefaultService.deleteVisit(parseInt(this.visit_id));
    //   this.$router.back();
    // },
    async updateVisit() {
      // TODO
      if (!this.visit) {
        return;
      }
      const visit = this.visit;
      this.visit = undefined;
      // this.visit = await DefaultService.updateVisit(this.visit_id, visit.visit);
    },
  },
  mounted() {
    this.fetchVisit();
  },
  props: {
    visit_id: {
      type: Number,
      required: true,
    },
  },
};
</script>
