// Main page of visit booking process.
// Visit page is in control of fetching the data and setting the props of other components
// Other pages are considered sub-pages and are not independant

<template>
  <div 

  >
    <wide-header title="Онлайн-запись" />
        
    <form v-if="current_screen=='start'">
      <ul>
        <li>
          <button v-on:click="changeCurrentScreen('visit-select-service')" ><img src="../assets/list-icon.jpg">Услуга</button>

          <span v-if="checked_services.length != 0"> 
                <p v-for="service in checked_services" :key="service.id">
                  {{service.name}} {{service.price}} {{service.currency}}
                </p>
          </span>

        </li>
        <li>
          <button v-on:click="changeCurrentScreen('visit-select-worker')" ><img src="../assets/worker-icon.png">Сотрудник</button>

          <span v-if="worker!=null" class="selected">
            {{ worker.name }}
          </span>

        </li>
        <li v-show="(checked_services.length > 0)">
          <button v-on:click="changeCurrentScreen('visit-select-datetime')" ><img src="../assets/calendar-icon.png">Дата и время</button>
          <span v-if=" visit_time != null " class="selected">
            Дата и время {visit_time}
          </span>
        </li>
      </ul>
          <input type="button" value="Сформировать запись" name="create-visit" id="create-visit">
    </form>

    <visit-select-service      
      v-if="current_screen=='visit-select-service'"  
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:check-services="applyCheckedServices"
      v-bind:services="services"
    />
    <visit-select-worker   
      v-if="current_screen=='visit-select-worker'"
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:select-worker=applySelectedWorker
      v-bind:workers="workers"
    />
    <visit-select-datetime
      v-if="current_screen=='visit-select-datetime'" 
      v-on:go-start-screen="changeCurrentScreen('start')"
      v-on:select-date="applySelectedDate"
      v-bind:availability="availability"
    />
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import WideHeader from "@/components/WideHeader.vue";
import VisitSelectDatetime from '@/components/VisitSelectDatetime.vue';
import VisitSelectService from '@/components/VisitSelectService.vue';
import VisitSelectWorker from '@/components/VisitSelectWorker.vue';

import availability_mock from "@/mocks/availability_mock.js"
import services_mock from "@/mocks/services_mock.js"
import workers_mock from "@/mocks/workers_mock.js"

export default {
    components: { WideHeader, VisitSelectDatetime, VisitSelectService, VisitSelectWorker },
    data () { 
        var availability = null
        var services = []
        var workers = []
        if (process.env.VUE_APP_OFFLINE == true) {
            availability = availability_mock["mock"]
            services = services_mock["mock"]
            workers = workers_mock["mock"]
        }
        return { 
            "availability": availability, 
            "checked_services": [],
            "client_id": null,  // sets when mounted
            "current_screen": "start",
            "services": services,
            "visit_time": null,
            "worker": null,
            "workers": workers,
            // todo: add loading (passed to child components and renders loading screen while something is loaded)
            // todo: expose selection in the path; https://forum.vuejs.org/t/how-to-restore-the-exact-state-of-a-route-when-clicking-the-back-button/109105/6
        }
    },
    computed: {
      checkedServicesIds() {
        return this.checked_services.map(s => { return s.service_id })
      }
    },
    mounted() {
      this.client_id = this.$route.query.org || null;  // setting null to avoid undefined
      
      this.getWorkers();
      this.getServices();
      // alert(`client_id ${this.client_id}`)
    },
    methods: {
        changeCurrentScreen: function (x) { console.log('Change screen!', x); this.current_screen = x},
        // todo: flush selection (something has been selected, current availability might be wrong)
        applyCheckedServices: function (x) { 
          this.checked_services = x;
          this.getAvailability();
        },
        applySelectedWorker: function (x) { this.worker = x },
        applySelectedDate: function (date, slots) {
          // todo: slots are parsed in a map atm, date: bool, not sure why did it, might be better to parse that into a simple array
          console(date, slots)
        },
        getWorkers() { 
         function handle_gw_error(error) {
            console.log(error);
          }
          function _handle_gw_response(response) {
              // notice - this is bound to the function below 
              if (response.data == null) {
                  console.log('Got workers', response); 
                  alert('Empty')
              }
              else {
                  let workers = response.data.workers; 
                  console.log('Got workers', response); 
                  this.workers = this.parseWorkers(workers);  
              }
          }
          const handle_gw_response = _handle_gw_response.bind(this)

          let path = `/client/${this.client_id}/workers`
          this.$api.get(
            path,
          )
          .then(handle_gw_response).catch(handle_gw_error)
        },
        parseWorkers(w) {
          // todo
          console.log(w)
          return w;
        },
        getServices() {
          function handle_gs_error(error) {
            console.log(error);
          }

          function _handle_gs_response(response) {
              // notice - this is bound to the function below 
              if (response.data == null) {
                  console.log('Got services', response); 
                  alert('Empty')
              }
              else {
                  let services = response.data.services; 
                  console.log('Got services', response); 
                  this.services = this.parseServices(services);  
              }
          }
          const handle_gs_response = _handle_gs_response.bind(this)

          let path = `/client/${this.client_id}/services`
          this.$api.get(
            path,
            // no need for auth here, keeping for example use
            // {"headers": {'Authorization': 'bearer ' + this.$store.state.jwt_auth}}
          )
          .then(handle_gs_response).catch(handle_gs_error)
        },
        parseServices(s) {
          // todo
          console.log(s)
          return s;
        },
        getAvailability() {
          // sets this.availability

          // todo: check if called in offline
          function handle_av_error(error) {
            console.log(error);
          }
          function _handle_av_response(response) {
              if (response.data == null) {
                  console.log('GOT AVAILABILITY', response); 
                  alert('Empty')
              }
              else {
                  let availability = response.data.availability; 
                  console.log('GOT AVAILABILITY', response); 
                  this.availability = this.parseAvailability(availability);  
              }
          }
          const handle_av_response = _handle_av_response.bind(this)

          console.log('Getting availability',)
          let path = `/client/${this.client_id}/availability`
          if (this.worker != null) {
            path = `/client/${this.client_id}/worker/${this.worker.worker_id}/availability`
          }
          if (this.checked_services.length > 0) {
            path += `?services=${this.checkedServicesIds.join(",")}`
          }
          // todo add workers 
          this.$api.get(
            path,
            // no need for auth here, keeping for example use
            // {"headers": {'Authorization': 'bearer ' + this.$store.state.jwt_auth}}
          )
          .then(handle_av_response).catch(handle_av_error)
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
