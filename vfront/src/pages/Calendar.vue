<template>
  <div class="main">
    <wide-header title="Выбор даты"></wide-header>
    <button class="left" @click="moveToPrevMonth">
      <img class="left" src="../assets/arrow2.png" />
    </button>
    <div class="month">Ноябрь 2021</div>
    <button class="right" @click="moveToNextMonth">
      <img class="right" src="../assets/arrow2.png" />
    </button>
    <p> Пн, вт, ср, чт, пт, сб, вс </p>
    <div v-if="availability == null"> Loading ... </div>
    <div v-if="availability != null" class="dates">
    <span v-for="day in calendar_dates" :key=day.getTime() v-bind:class="{clickable: isAvailable(day)}" >{{ day.getUTCDate() }}</span>
    </div>
    <br />
    <div class="explication">
        <!-- clickable cell - class="clickable" -->
      <span class="square clickable"></span>
      <span class="description">- дата доступна для выбора</span>
      <br /><br />
        <!-- nonclickacle - usual cell  -->
      <span class="square"></span>
      <span class="description">- дата не доступна для выбора</span>
        <!-- class="empty" for empty cells -->
    </div>
    
    <!-- <p> Это временно, потом уберу, бусь </p> -->
    <!-- {{ availability }} -->
  </div>
</template>

<script>
import WideHeader from "../components/WideHeader.vue";
export default {
    data() { 
        return {
            'availability': null, 
            'calendar_start_date': new Date(),
            'calendar_dates': [],
            'no_backend': true,
        } 
    },
    components: { WideHeader },
    methods: {
        getAvailability() {
            console.log('Getting availability',)
            this.$api.get('/client_availability/1?service_id=1', {"headers": {'Authorization': 'bearer ' + this.$store.state.jwt_auth}})
            .then(response => { 
                if (response.data == null) {
                    console.log('GOT AVAILABILITY', response); 
                    alert('Empty')
                }
                else {
                    let availability = response.data.availability; 
                    console.log('GOT AVAILABILITY', response); 
                    this.availability = this.parseAvailability(availability);  
                }
            }).catch(e => console.log(e))
        },
        parseAvailability(a) {
            console.log('Parsing...', a)
            const av = {}
            for (const worker_av of Object.values(a)) {
                // console.log('worker_av', worker_av)
                for (const row of worker_av['days']) {
                    // console.log('row', row)
                    const dt = row['date']
                    for (const ts of row['timeslots'] ) {
                        let _date
                        if (av[dt] != null) {_date = av[dt]}
                        else {_date = {};}
                        const from = ts['dt_from']
                        _date[from] = true;
                        av[dt] = _date
                    }
                }
            }
            console.log('Parsed')

            return av
        },
        findCalendarBase(_date) {
            // finds a cell to begin calendar with (Monday which is 1st in current month or prior to that)
            let date = new Date(_date)

            date.setUTCDate(1)
            console.debug('Here', date)
            for (;;) {
                if (date.getUTCDay() == 1) { break }
                date = new Date(date.getTime() - (1000 * 60) * 60 * 24)  // (miliseconds * seconds)... 24h
            }
            console.log('Base date', date)
            return date 
        },
        listCalendarDatesFromBase(_date) {
            // returns 5 weeks of days
            let date = new Date(_date)

            const dates = [];
            for (let i = 0; i<35; i++) {
                date = new Date(date.getTime() + ((1000 * 60) * 60 * 24))  // 24h
                dates.push(date)
            }
            console.log('Calendar dates', dates)
            return dates
        },
        updateCalendarDates() {
            console.log('Rendering from', this.calendar_start_date);
            const base = this.findCalendarBase(this.calendar_start_date);
            const calendar_dates = this.listCalendarDatesFromBase(base);
            this.calendar_dates = calendar_dates
        },
        IsLessThenToday(date) {
            const today = new Date()
            return date > today;
        },
        isAvailable(date){
            // validates date against calendar and availability
            if (this.IsLessThenToday(date)) { return false }
            
            return true
        },
        moveToNextMonth() {
            const date = this.calendar_start_date;
            const month = date.getUTCMonth();
            this.calendar_start_date.setUTCMonth(month + 1)

            this.updateCalendarDates()

        },
        moveToPrevMonth() {
            console.log('MOVIT')
            const date = this.calendar_start_date;
            const month = date.getUTCMonth();
            this.calendar_start_date.setUTCMonth(month - 1)
            console.log(this.calendar_start_date)

            this.updateCalendarDates()
        },
    },
    created() {
        console.debug('Created Calendar page')
        if (this.no_backend) {
            this.availability = true
        } else {
            this.getAvailability()
        }
        this.updateCalendarDates()
    }
}

</script>
<style scoped src="@/assets/styles/calendar.css"></style>
