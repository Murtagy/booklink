<template>
  <div class="main">
    <wide-header title="Выбор даты"></wide-header>
    <button class="left" @click="moveToPrevMonth">
      <img class="left" src="../assets/arrow2.png" />
    </button>
    <div class="month"> {{ months_rus[calendar_start_date.getMonth()] }} {{ calendar_start_date.getFullYear() }}</div>
    <button class="right" @click="moveToNextMonth">
      <img class="right" src="../assets/arrow2.png" />
    </button>
    <div v-if="availability == null"> Loading ... </div>
    <div v-if="availability != null" class="dates">
    <span class=day>Пн</span><span class=day>Вт</span><span class=day>Ср</span><span class=day>Чт</span><span class=day>Пт</span><span class=day>Сб</span><span class=day>Вс</span>
    <span v-for="day in calendar_dates" :key=day.getTime() v-bind:class="{clickable: isAvailable(day), empty: isNotSelectedMonth(day)}" class=dates>{{ isNotSelectedMonth(day) ? '' : day.getUTCDate() }}</span>
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

const months_rus = {
    0:  'Январь'  ,
    1:  'Февраль' ,
    2:  'Март'    ,
    3:  'Апрель'  ,
    4:  'Май'     ,
    5:  'Июнь'    ,
    6:  'Июль'    ,
    7:  'Август'  ,
    8:  'Сентябрь',
    9:  'Октябрь' ,
    10: 'Ноябрь'  ,
    11: 'Декабрь' ,
}

export default {
    data() { 
        const today = new Date()
        return {
            'availability': null, 
            'calendar_start_date': today,
            'calendar_dates': [],
            'no_backend': true,
            'months_rus': months_rus,
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
            // @bug
            // here might be a bug in comparison, e.g. date with current timestamp compared with almost the same date
            // triggered when updating the page fast enough
            const today = new Date()
            return date < today;
        },
        isAvailable(date){
            // validates date against calendar and availability
            if (this.IsLessThenToday(date)) { return false }
            if (this.isNotSelectedMonth(date)) { return false }
            
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
        isNotSelectedMonth(date){
            return (date.getUTCMonth() != this.calendar_start_date.getUTCMonth())
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
