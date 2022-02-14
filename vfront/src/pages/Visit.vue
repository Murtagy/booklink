<template>
  <div 

  >
    <wide-header title="Онлайн-запись" />
        
    <form v-if="current_screen=='start'">
      <ul>
        <li>
          <button v-on:click="changeCurrentScreen('visit-select-service')" ><img src="../assets/list-icon.jpg">Услуга</button>

          <div v-if="services.length != 0"> 
              <ul>
                <li v-for="service in services" :key="service.id">
                  {{service.name}} {{service.price}} {{service.currency}}
                </li>
              </ul>
          </div>

        </li>
        <li>
          <button v-on:click="changeCurrentScreen('visit-select-worker')" ><img src="../assets/worker-icon.png">Сотрудник</button>

          <div v-if="worker!=null" class="selected">
            {{ worker.name }}
          </div>

        </li>
        <li>
          <button v-on:click="changeCurrentScreen('visit-select-datetime')" ><img src="../assets/calendar-icon.png">Дата и время</button>
          <div v-if=" visit_time != null " class="selected">
            Дата и время
          </div>
        </li>
      </ul>
          <input type="button" value="Сформировать запись" name="create-visit" id="create-visit">
    </form>

    <visit-select-datetime
      v-if="current_screen=='visit-select-datetime'" 
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:select-date="applySelectedDate"
      v-bind:availability="availability"
    />
    <visit-select-service      
      v-if="current_screen=='visit-select-service'"  
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:check-services="applyCheckedServices"
    />
    <visit-select-worker   
      v-if="current_screen=='visit-select-worker'"
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:select-worker=applySelectedWorker
    />
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import WideHeader from "@/components/WideHeader.vue";
import VisitSelectDatetime from '@/components/VisitSelectDatetime.vue';
import VisitSelectService from '@/components/VisitSelectService.vue';
import VisitSelectWorker from '@/components/VisitSelectWorker.vue';

export default {
    components: { WideHeader, VisitSelectDatetime, VisitSelectService, VisitSelectWorker },
    data () { 
        return { 
            // visit-type-form, visit-select- service/worker/datetime
            'availability': null, 
            "current_screen": "start",
            "worker": null,
            "services": [],
            "visit_time": null,
        }
    },
      // created() {
      //   console.debug('Created Calendar page')
      //   if (this.no_backend) {
      //       this.availability = true
      //   } else {
      //       this.getAvailability()
      //   }
      //   // this.updateCalendarDates()
      // },
    methods: {
        changeCurrentScreen: function (x) { console.log('Change screen!', x); this.current_screen = x},
        applyCheckedServices: function (x) { 
          this.services = x;
          this.getAvailability();
        },
        applySelectedWorker: function (x) { this.worker = x },
        applySelectedDate: function (date, slots) {
          // todo: slots are parsed in a map atm, date: bool, not sure why did it, might be better to parse that into a simple array
          console(date, slots)
        },
        getAvailability() {
            // sets this.availability
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
    }
};
</script>
