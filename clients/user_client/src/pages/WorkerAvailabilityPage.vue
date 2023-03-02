<template>
  <div class="box">
    Время работы
    <div v-for="slot in slots">
      <input :value="formatTime(slot.dt_from)" style="max-width: 4em" /> -
      <input :value="formatTime(slot.dt_to)" style="max-width: 4em" />
    </div>
    <form id="potential_slot" @submit.prevent="submitPotentialSlot">
      <input v-model="potential_slot.dt_from" style="max-width: 4em; background:ghostwhite" /> -
      <input v-model="potential_slot.dt_to" style="max-width: 4em; background:ghostwhite" />
      <input type="submit" value="+" />
    </form>
    <div>
      <input type="button" :value="save_text" @click="save"/>
    </div>
    <div>
      <input type="button" value="Применить ко дням" />
    </div>
  </div>
  <div class="box">
    <div
      v-for="week in days_by_week"
      style="display: flex; flex-flow: row wrap; width: 100%"
    >
      <div
        v-for="day in week"
        :key="day.date"
        @click="dayClicked(day)"
        class="border_main1"
        style="width: 10em"
      >
        {{ day.date }}
        <br />
        <div v-for="timeslot in day.timeslots" :key="timeslot.dt_from">
          {{ formatTime(timeslot.dt_from) }} - {{ formatTime(timeslot.dt_to) }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

<script lang="ts">
import {
  DefaultService,
  TimeSlotType,
  type Day,
  type TimeSlot,
} from "@/client";

export default {
  computed: {
    days_by_week() {
      let i = 0;
      const weeks: Day[][] = [];
      let week: Day[] = [];
      for (const day of this.days) {
        if (i % 7 == 0) {
          weeks.push(week);
          week = [];
        }
        week.push(day);
        i += 1;
      }
      return weeks;
    },
    save_text(): string {
      return `Сохранить ${this.day.date}`;
    },
  },
  components: {
    // VisitsDayCaruselDay
  },
  data() {
    const day: Day = {date: '', timeslots: []}
    const days: Day[] = [];
    const highlighted: Day[] = [];
    const slots: TimeSlot[] = [];
    const today = new Date();
    const startOfMonth = today.toISOString().split("T")[0].slice(0, 8) + "01";
    return {
      from: startOfMonth,
      day: day,
      days: days,
      highlighted: highlighted,
      potential_slot: {
        dt_from: "",
        dt_to: "",
      },
      slots: slots,
    };
  },
  mounted() {
    this.fetchDays();
  },
  methods: {
    async dayClicked(day: Day) {
      this.slots = day.timeslots;
      this.day.date = day.date;
    },
    async fetchDays() {
      this.days = (
        await DefaultService.getWorkerAvailabilityByUser(
          this.worker_id,
          this.from
        )
      ).days;
    },
    formatTime(time: string) {
      if (time.length == 5) {
        return time
      }
      return time.slice(11, 16);
    },
    async save() {
      const date = this.day.date

      if (date) {
        // single day save
        const new_slots: TimeSlot[] = [...this.slots]
        // this.slots = []
        for (const slot of new_slots) {
          if (slot.dt_from.length == 5) {
            // transform potential slot into app slot (full timestamp)
            slot.dt_from = date + "T" + slot.dt_from + ":00"
            slot.dt_to = date + "T" + slot.dt_to + ":00"
          }
        }
        await DefaultService.createWorkerAvailability(this.worker_id, {days: [{date: this.date, timeslots: new_slots}]})
        this.day.timeslots = new_slots
      }
    },
    async submitPotentialSlot() {
      this.slots.push({
        dt_from: this.potential_slot.dt_from,
        dt_to: this.potential_slot.dt_to,
        slot_type: TimeSlotType.AVAILABLE,
      });
      this.potential_slot = {
        dt_from: "",
        dt_to: "",
      };
    },
  },
  props: {
    worker_id: {
      type: String,
      required: true,
    },
  },
  watch: {
    potential_slot: {
      handler(newSlot, oldSlot) {
        const slot = newSlot
        if (slot.dt_from.length > 2 && slot.dt_from[2] != ':' ) {
          slot.dt_from = slot.dt_from.slice(0,2) + ':' + slot.dt_from.slice(2)
        }
        if (slot.dt_to.length > 2 && slot.dt_to[2] != ':' ) {
          slot.dt_to = slot.dt_to.slice(0,2) + ':' + slot.dt_to.slice(2)
        }
      },
      deep: true
    }
  }
};
</script>
