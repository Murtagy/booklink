<template>
	<FunctionalCalendar
      v-model="calendarData"
      :configs="calendarConfigs"
	></FunctionalCalendar>
</template>
      
<script>

import { FunctionalCalendar } from 'vue-functional-calendar';
export default {
    components: {
        FunctionalCalendar
    },
  data() {
        return {
            calendarData: {},
            calendarConfigs: {
                sundayStart: true,
                dateFormat: 'dd/mm/yyyy',
                isDatePicker: false,
                isDateRange: false,
                disabledDayNames: "['Su', 'We']",
                disabledDates: ['beforeToday', '12/10/2021'],
            }
        }
    },
}

</script>