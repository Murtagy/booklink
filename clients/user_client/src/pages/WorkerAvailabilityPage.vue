<template>
  <div class="box">
    <i 
      class="fa-solid fa-question"
      @click="showHelp = !showHelp"
      style="float: right; overflow: auto"
    >
      <div v-show="showHelp" 
        class="border_main1"
        style="margin-botton: 1em"
      > 
      <p>Для выбора времени работы нажмите на требуемый день, затем введите время работы и нажмите на кнопку сохранить. </p>
      <p>Чтобы сохранить сразу несколько дней времени работы, введите время работы, затем нажмите на кнопку "Применить ко дням". Нажмите на нужные дни и нажмите на кнопку сохранить.</p>
      <p>Нажмите на вопросительный знак еще раз чтобы закрыть обучение</p>

    </div>
    </i>
    <p class="bold">Время работы</p>
    <div style="margin-left: 1em">
      <div v-for="slot in slots" :key="slot.from_datetime">
        <input
          :value="formatTime(slot.from_datetime)"
          style="max-width: 4em"
          disabled="true"
        />
        -
        <input
          :value="formatTime(slot.to_datetime)"
          style="max-width: 4em"
          disabled="true"
        />
        <input type="button" value="-" @click="removeSlot(slot)" />
      </div>
      <form id="potential_slot" @submit.prevent="submitPotentialSlot">
        <input type="time" v-model="potential_slot.from_datetime" /> -
        <input type="time" v-model="potential_slot.to_datetime" />
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

    <todo> смена месяца </todo>
    <small><p><em>(оптимизировано под широкий экран)</em></p></small>
    <div
      v-for="week in days_by_week"
      :key="String(week)"
      style="display: flex; flex-flow: row wrap; width: 100%"
    >
      <div
        v-for="day in week"
        :key="day.date"
        @click="dayClicked(day)"
        class="border_main1"
        style="font-size: medium; margin: 1px; width: 7em"
        :class="{ highlighted: highlighted.indexOf(day) != -1, today: day.date == today }"
      >
        <div style="font-size: small">{{getDayDayOfWeek(day)}}</div>
        <div style="font-size: small">{{ day.date }}</div>
        <br />
        <div v-for="timeslot in day.timeslots" :key="timeslot.from_datetime">
          <div style="font-size: small; margin-top: 2px">
            {{ formatTime(timeslot.from_datetime) }} -
            {{ formatTime(timeslot.to_datetime) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.highlighted {
  background: rgba(51, 0, 82, 0.334);
}

.today {
  background: rgba(157, 0, 255, 0.143);
}

.activeButton {
  background: var(--color4);
  border: solid;
}
</style>

<script lang="ts">
import { DefaultService, SlotType, type Day, type TimeSlot } from "@/client";
import dayjs from "dayjs";

const emptyDay = () => {
  return { date: "", timeslots: [] };
};


export default {
  dayjs: dayjs,
  computed: {
    today(): string {
      return dayjs().format('YYYY-MM-DD')
    },
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
        from_datetime: "",
        to_datetime: "",
      },
      slots: slots,
      showHelp: false,
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
          this.potential_slot = { from_datetime: "", to_datetime: "" };
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
    getDayDayOfWeek(d: Day) {
      const daysOfWeek = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
      const date = dayjs(d.date);
      const dayOfWeek = date.day();
      const dayOfWeekString = daysOfWeek[dayOfWeek];
      return dayOfWeekString;
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
          slot.from_datetime =
            date + "T" + this.formatTime(slot.from_datetime) + ":00";
          slot.to_datetime =
            date + "T" + this.formatTime(slot.to_datetime) + ":00";
        }
        if (
          this.potential_slot.from_datetime &&
          this.potential_slot.to_datetime
        ) {
          const slot = {
            from_datetime:
              date +
              "T" +
              this.formatTime(this.potential_slot.from_datetime) +
              ":00",
            to_datetime:
              date +
              "T" +
              this.formatTime(this.potential_slot.to_datetime) +
              ":00",
            slot_type: SlotType.AVAILABLE,
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
              from_datetime:
                date + "T" + this.formatTime(slot.from_datetime) + ":00",
              to_datetime:
                date + "T" + this.formatTime(slot.to_datetime) + ":00",
              slot_type: SlotType.AVAILABLE,
            };
            new_day_slots.push(new_slot);
          }
          if (
            this.potential_slot.from_datetime &&
            this.potential_slot.to_datetime
          ) {
            const slot = {
              from_datetime:
                date +
                "T" +
                this.formatTime(this.potential_slot.from_datetime) +
                ":00",
              to_datetime:
                date +
                "T" +
                this.formatTime(this.potential_slot.to_datetime) +
                ":00",
              slot_type: SlotType.AVAILABLE,
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
      if (
        !(this.potential_slot.from_datetime && this.potential_slot.to_datetime)
      ) {
        return;
      }
      this.slots.push({
        from_datetime: this.potential_slot.from_datetime,
        to_datetime: this.potential_slot.to_datetime,
        slot_type: SlotType.AVAILABLE,
      });
      this.potential_slot = {
        from_datetime: "",
        to_datetime: "",
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
        if (slot.from_datetime.length > 2 && slot.from_datetime[2] != ":") {
          slot.from_datetime =
            slot.from_datetime.slice(0, 2) + ":" + slot.from_datetime.slice(2);
        }
        if (slot.to_datetime.length > 2 && slot.to_datetime[2] != ":") {
          slot.to_datetime =
            slot.to_datetime.slice(0, 2) + ":" + slot.to_datetime.slice(2);
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
