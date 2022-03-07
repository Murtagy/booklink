<template>    
    <div>
        <calendar v-if="screen=='calendar'"
            v-bind:availability=availability
            v-bind:availability_mode=availability_mode
            v-on:pick-date="pickDate"
        />
        <TimeSched v-if="screen=='time'"
            v-bind:date=selected_date
            v-bind:timeslots=timeslots
        />
    </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import Calendar from "@/pages/Calendar"
import TimeSched from "@/pages/Time"

export default {
    components: { Calendar, TimeSched },
    data() { 
        return {
            "availability_mode": true,
            "screen": 'calendar',
            "selected_date": null,
            "timeslots": null,
        } 
    },
    props: ['availability'],
    methods: {
        pickDate(x) {
            console.log('Picked date', x)
            const _date = new Date(x)
            this.selected_date = _date
            const date = this.selected_date.toISOString().split("T")[0];

            this.timeslots = this.availability[date]
            this.screen = 'time'
        }
    }

}

</script>
