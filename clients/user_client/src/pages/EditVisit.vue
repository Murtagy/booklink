<template>
  <div v-if="visit">
    <form @submit.prevent="updateVisit" class="border_main1">
      <div>
        Услуги:
        <span v-for="service of visit.services" :key="service.service_id">
          {{ service.name }}
        </span>
        <span v-if="visit.services.length > 0"> Не указаны </span>
      </div>
      <br />
      <div>
        <section class="bold">Данные о клиентe:</section>
        <div id="client_data" style="padding-left: 1em">
          <label v-if="render_bad_phone" style="color: crimson" for="phone">
            Телефон РБ с кодом
          </label>
          <section>
            Телефон - <input type="tel" v-model="user_phone" id="phone" />
          </section>
          <section>Email - <input type="email" v-model="user_email" /></section>
        </div>
      </div>
      <button class="save" type="submit">Сохранить</button>
      <div style="clear: both"></div>
    </form>

    <br />
    <form @submit.prevent="updateTime" class="border_main1">
      <button
        v-if="!show_cancel"
        @click="show_cancel = !show_cancel"
        style="float: right; color: crimson"
        type="submit"
      >
        Отменить
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
      <div v-if="!show_cancel">
        <label for="visit_from_time">Время начала визита </label>
        <input
          id="visit_from_time"
          type="time"
          v-model="user_from_time"
          required
        />
        <br />
        <label for="visit_to_time">Время конца визита </label>
        <input id="visit_to_time" type="time" v-model="user_to_time" required />
        <br />
        <label for="let_customer_know"> Отправить уведомления </label>
        <input type="checkbox" id="let_customer_know" v-model="notify" />
        <button class="save" type="submit">Обновить время</button>
        <div style="clear: both"></div>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { DefaultService, type OutVisitExtended } from "@/client";
import { extended_visit_repr } from "@/extended_visit_repr";
import dayjs from "dayjs";

import { sanitize_phone } from "@/sanitize_phone";
import { validate_phone } from "@/validate_phone";

declare interface Data {
  render_bad_phone: boolean;
  render_bad_email: boolean;
  show_cancel: boolean;
  user_from_time: string;
  user_to_time: string;
  user_phone: string;
  user_email: string;
  visit?: OutVisitExtended;
  notify: boolean;
}

export default {
  components: {},
  computed: {
    cancelYes(): string {
      if (!this.visit) {
        return "";
      }
      const visit_repr = extended_visit_repr(this.visit);
      return `Да, отменить визит, ${visit_repr}`;
    },
    email(): string {
      if (this.visit) {
        const email = this.visit.visit.email;
        if (email) {
          return email;
        }
      }
      return "Не указан";
    },
    phone(): string {
      if (this.visit) {
        const phone = this.visit.visit.phone;
        if (phone) {
          return phone;
        }
      }
      return "Не указан";
    },
  },
  data(): Data {
    return {
      show_cancel: false,
      visit: undefined,
      render_bad_phone: false,
      render_bad_email: false,
      user_phone: "",
      user_email: "",
      user_from_time: "",
      user_to_time: "",
      notify: false,
    };
  },
  methods: {
    async cancelVisit() {
      // TODO
    },
    async fetchVisit() {
      this.visit = await DefaultService.getVisitExtended(this.visit_id);
      this.user_from_time = dayjs(this.visit.visit.from_datetime).format(
        "HH:mm"
      );
      this.user_to_time = dayjs(this.visit.visit.to_datetime).format("HH:mm");
      if (this.visit.visit.phone) {
        this.user_phone = this.visit.visit.phone;
      }
      if (this.visit.visit.email) {
        this.user_email = this.visit.visit.email;
      }
    },
    async updateTime() {
      if (this.visit) {
        const from_hh_mm = this.user_from_time.split(":");
        const to_hh_mm = this.user_to_time.split(":");

        const new_from = dayjs(this.visit.visit.from_datetime)
          .set("hour", parseInt(from_hh_mm[0]))
          .set("minute", parseInt(from_hh_mm[1]));
        const new_to = dayjs(this.visit.visit.to_datetime)
          .set("hour", parseInt(to_hh_mm[0]))
          .set("minute", parseInt(to_hh_mm[1]));

        await DefaultService.updateSlot(this.visit_id, {
          from_datetime: new_from.toISOString(),
          to_datetime: new_to.toISOString(),
          notify: this.notify,
        });

        await this.fetchVisit();
        await this.$router.back();
      }
    },
    async updateVisit() {
      if (!this.visit) {
        return;
      }
      let user_phone: string | undefined = sanitize_phone(this.user_phone);
      this.render_bad_phone = false;
      if (user_phone) {
        if (!validate_phone(user_phone)) {
          this.render_bad_phone = true;
        }
      } else {
        user_phone = undefined;
      }

      let user_email: string | undefined = sanitize_phone(this.user_email);
      this.render_bad_email = false;
      if (user_email) {
        if (!user_email.includes("@")) {
          this.render_bad_email = true;
        }
      } else {
        user_email = undefined;
      }
      if (this.render_bad_email || this.render_bad_phone) {
        return;
      }

      await DefaultService.updateSlotCustomerInfo(this.visit_id, {
        phone: user_phone,
        email: user_email,
      });
      await this.fetchVisit();
      await this.$router.back();
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
