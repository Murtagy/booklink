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

    <visit-select-datetime v-if="current_screen=='visit-select-datetime'" />
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
            "current_screen": "start",
            "worker": null,
            "services": [],
            "visit_time": null,
        }
    },
    methods: {
        changeCurrentScreen: function (x) { console.log('Change screen!', x); this.current_screen = x},
        applyCheckedServices: function (x) { this.services = x },
        applySelectedWorker: function (x) { this.worker = x },
    }
};
</script>
