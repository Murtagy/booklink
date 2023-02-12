<template>
  <div class="box" >
    <div v-if="!submitted">
      <form>
        <div id="inputs">
        <p class="bold"><label for="phone">Номер телефона (мобильный): </label></p>
        <input
          id="phone" name="phone"
          placeholder="375-29-1234567"
          type="tel"
          v-model="phone"
        /> 
        <label v-show="bad_phone" class="danger" > Телефон РБ с кодом</label>

        <p class="bold"><label for="email">Email</label></p>
        <input
          id="email" name="email"
          placeholder="email@example.com"
          type="email"
          v-model.trim="email"
        />

        <p class="bold"><label for="first_name">Ваши фамилия и имя</label></p>
        <input
          id="last_name" name="last_name"
          placeholder="Фамилия"
          type="last_name"
          v-model.trim="last_name"
        />
        <input
          id="first_name" name="first_name"
          placeholder="Имя"
          type="first_name"
          v-model.trim="first_name"
        />

        <p class="bold"><label for="remind_me"> Напомнить о записи? </label></p>
        <input type="checkbox" v-model="remind_me"/>
      </div>
      </form>
      <!-- <p>{{services}}</p> -->
      <p class="bold">Выбранные услуги:</p>
      <li v-for="service in services" :key="service.service_id">
        <label :for="String(service.service_id)">{{ service.name }}</label>
        <span class="price">{{ service.price }} {{ service.currency }}</span>
      </li>

      <!-- <p>{{visit_time}}</p> -->
      <p class="bold">Время:</p>
      <p class="border_main1" style="padding: 1em">
        {{ parse_date() }}
      </p>
      <!-- <p>{{worker}}</p> -->
      <p class="bold">Запись к:</p>
      <div class="cards">
        <div class="card">
          <p class="border_main1" style="padding: 1em">
          <div v-if="worker">
            {{ worker.name }}, {{ worker.job_title }}
          </div>
          <div v-else >
              Не важно
          </div>
          </p>
        </div>
      </div>

      <input type="button" value="Подтвердить запись" class="sticky_button" @click="submit_visit"/>
    </div>
    <div v-else>
      <div v-if="error">
        {{ error }}
      </div>
      <div v-else>
        <div v-if="!booked_visit">
          Загрузка...
        </div>
        <div v-else>
          {{booked_visit.phone}}
          ...
          <!-- TODO: more visit info -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
li {
  display: block;
  margin: 0px;
  margin-top: 1px;
  padding: 5px;
  padding-top: 15px;
  padding-bottom: 15px;
  border: 2px solid var(--color1);
  position: relative;
}
p.bold {
  font-weight: bold;
}

.danger {
  color: rgb(255, 162, 0);
}

#inputs {
  border: 2px solid var(--color1);
  padding: 0.5em;
}
</style>

<script lang="ts">
import type { OutWorker } from "@/client/models/OutWorker"
import type { OutService } from "@/client/models/OutService"
import {sanitize_phone} from "@/sanitize_phone";
import {validate_phone} from "@/validate_phone";
import type { PropType } from 'vue'
import { TimeSlot } from "@/models/availability/TimeSlot";
import { DefaultService } from "@/client/services/DefaultService";
import type { InServiceToVisit } from "@/client/models/InServiceToVisit";
import type { OutVisit } from "@/client/models/OutVisit";

declare interface ComponentData {
  booked_visit: null | OutVisit,
  error: string,
  first_name: string,
  last_name: string,
  phone: string,
  email: string,
  remind_me: boolean,
  submitted: boolean,
}
export default {
  components: {},
  data(): ComponentData {
    return {
      booked_visit: null,
      error: "",
      first_name: "",
      last_name: "",
      phone: "",
      email: "",
      remind_me: true,
      submitted: false,
    };
  },
  computed: {
    bad_phone(): boolean {
      const phone = sanitize_phone(this.phone);
      return !validate_phone(phone)
    },
    services_to_visit(): InServiceToVisit[] {
      const services_to_visit: InServiceToVisit[] = []
      for (const service of this.services) {
        services_to_visit.push({service_id: service.service_id})
      }
      return services_to_visit
    }
  },
  methods: {
    parse_date() {
      if (this.visit_slot != null) {
        const date = new Date(this.visit_slot.dt_from);
        const day = `${String(date.getFullYear())}-${String(
          date.getMonth()
        ).padStart(2, "0")}-${String(date.getDay()).padStart(2, "0")}`;
        const time = `${String(date.getHours())}:${String(
          date.getMinutes()
        ).padStart(2, "0")}`;
        return `${day} ${time}`;
      }
      return "-";
    },
    async submit_visit() {
      this.submitted = true
      try {
        const visit = await DefaultService.publicBookVisit(
          {
            client_id: this.client_id,
            email: this.email,
            first_name: this.first_name,
            from_dt: this.visit_slot.dt_from,
            last_name: this.last_name,
            phone: this.phone,
            remind_me: this.remind_me,
            services: this.services_to_visit,
            worker_id: this.worker?.worker_id,
          }
        )
        this.booked_visit = visit
      } catch (error) {
        // TODO: type out errors
        // slot conflict = http_409
        console.log(error)
        this.error = 'Увы, что-то пошло не так, возможно время уже не доступно. Попробуйте записаться еще раз.'
      }
    }
  },
  props: {
    worker: {
      type: Object as PropType<OutWorker>,
    },
    visit_slot: {
      type: TimeSlot, required: true
    },
    services: {
      type: Array<OutService>, required: true
    },
    client_id: {
      type: Number, required: true
    }
  },
};
</script>
