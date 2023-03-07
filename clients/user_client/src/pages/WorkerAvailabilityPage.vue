<template>
  <div class="box">
    <p class="bold">Время работы</p>
    <div style="margin-left: 1em">
      <div v-for="slot in slots" :key="slot.dt_from">
        <input
          :value="formatTime(slot.dt_from)"
          style="max-width: 4em"
          disabled="true"
        />
        -
        <input
          :value="formatTime(slot.dt_to)"
          style="max-width: 4em"
          disabled="true"
        />
        <input type="button" value="-" @click="removeSlot(slot)" />
      </div>
      <form id="potential_slot" @submit.prevent="submitPotentialSlot">
        <input type="time" v-model="potential_slot.dt_from"  /> -
        <input type="time" v-model="potential_slot.dt_to"  />
        <input type="submit" value="+" />
      </form>
      <div>
        <input type="button" :value="save_text" @click="save" />
      </div>
      <div>
        <input
          type="button"
          value="Применить ко дням"
          @click="manyMode = !manyMode"
          :class="{ activeButton: manyMode }"
        />
      </div>
    </div>
  </div>
  <div class="box">
    <!-- todo: solve :key -->
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
        :class="{ highlighted: highlighted.indexOf(day) != -1 }"
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

<style scoped>
.highlighted {
  background: dimgray;
}

.activeButton {
  background: var(--color4);
  border: solid;
}
</style>

<script lang="ts">
import {
  DefaultService,
  TimeSlotType,
  type Day,
  type TimeSlot,
} from "@/client";

const emptyDay = () => {
  return { date: "", timeslots: [] };
};
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
      if (this.highlighted.length) {
        return `Сохранить ${this.highlighted.length} дней`;
      }
      if (this.day.date) {
        return `Сохранить ${this.day.date}`;
      }
      return "День не выбран";
    },
  },
  components: {
    // VisitsDayCaruselDay
  },
  data() {
    const day: Day = emptyDay();
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
      manyMode: false,
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
      if (this.manyMode) {
        if (this.highlighted.indexOf(day) == -1) {
          this.highlighted.push(day);
        } else {
          this.highlighted.splice(this.highlighted.indexOf(day), 1);
        }
      } else {
        if (day.timeslots.length) {
          this.slots = day.timeslots;
          this.potential_slot = { dt_from: "", dt_to: "" };
        }
        this.day.date = day.date;
      }
    },

    async fetchDays() {
      this.days = [];
      this.days = (
        await DefaultService.getWorkerAvailabilityByUser(
          this.worker_id,
          this.from
        )
      ).days;
    },

    formatTime(time: string) {
      if (time.length == 5) {
        return time;
      }
      return time.slice(11, 16);
    },

    async save() {
      if (!this.day.date && !this.highlighted.length) {
        return;
      }

      const new_days: Day[] = [];

      if (this.day.date && !this.highlighted.length) {
        const date = this.day.date;
        // single day save
        const new_slots = [...this.slots];
        for (const slot of new_slots) {
          slot.dt_from = date + "T" + this.formatTime(slot.dt_from) + ":00";
          slot.dt_to = date + "T" + this.formatTime(slot.dt_to) + ":00";
        }
        if (this.potential_slot.dt_from && this.potential_slot.dt_to) {
          const slot = {
            dt_from:
              date + "T" + this.formatTime(this.potential_slot.dt_from) + ":00",
            dt_to:
              date + "T" + this.formatTime(this.potential_slot.dt_to) + ":00",
            slot_type: TimeSlotType.AVAILABLE,
          };
          new_slots.push(slot);
        }
        new_days.push({ date: this.day.date, timeslots: new_slots });
        this.day.timeslots = new_slots;
        this.day.date = "";
      }
      if (this.highlighted.length) {
        // multiday save
        for (const day of this.highlighted) {
          const date = day.date;
          const new_day_slots: TimeSlot[] = [];
          for (const slot of this.slots) {
            const new_slot = {
              dt_from: date + "T" + this.formatTime(slot.dt_from) + ":00",
              dt_to: date + "T" + this.formatTime(slot.dt_to) + ":00",
              slot_type: TimeSlotType.AVAILABLE,
            };
            new_day_slots.push(new_slot);
          }
          if (this.potential_slot.dt_from && this.potential_slot.dt_to) {
            const slot = {
              dt_from:
                date +
                "T" +
                this.formatTime(this.potential_slot.dt_from) +
                ":00",
              dt_to:
                date + "T" + this.formatTime(this.potential_slot.dt_to) + ":00",
              slot_type: TimeSlotType.AVAILABLE,
            };
            new_day_slots.push(slot);
          }
          new_days.push({ date: date, timeslots: new_day_slots });
        }
        this.manyMode = false;
      }
      await DefaultService.createWorkerAvailability(this.worker_id, {
        days: new_days,
      });
      this.fetchDays();
    },
    async submitPotentialSlot() {
      if (!(this.potential_slot.dt_from && this.potential_slot.dt_to)) {
        return;
      }
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

    removeSlot(slot: TimeSlot) {
      this.slots = this.slots.filter((s) => s != slot);
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
        const slot = newSlot;
        if (slot.dt_from.length > 2 && slot.dt_from[2] != ":") {
          slot.dt_from = slot.dt_from.slice(0, 2) + ":" + slot.dt_from.slice(2);
        }
        if (slot.dt_to.length > 2 && slot.dt_to[2] != ":") {
          slot.dt_to = slot.dt_to.slice(0, 2) + ":" + slot.dt_to.slice(2);
        }
      },
      deep: true,
    },
    manyMode(newVal, oldVal) {
      if (newVal == false) {
        this.highlighted = [];
      }
    },
  },
};
</script>
