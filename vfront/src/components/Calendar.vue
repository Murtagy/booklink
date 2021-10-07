<template>
	<FunctionalCalendar
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
            calendarData: {}
        }
    }
}

</script>