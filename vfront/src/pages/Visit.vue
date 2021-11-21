<template>
  <div 
    v-on:visit-select="changeCurrentScreen" 
  >
    <wide-header title="Онлайн-запись" />
    <visit-type-form 
        v-on:visit-select="changeCurrentScreen" 
        v-if="current_screen=='visit-type-form'"
    />
    <visit-select-datetime v-if="current_screen=='visit-select-datetime'" />
    <visit-select-service  v-if="current_screen=='visit-select-service'"  />
    <visit-select-worker   v-if="current_screen=='visit-select-worker'"   />
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import WideHeader from "@/components/WideHeader.vue";
import VisitTypeForm from "@/components/VisitTypeForm.vue"
import VisitSelectDatetime from '@/components/VisitSelectDatetime.vue';
import VisitSelectService from '@/components/VisitSelectService.vue';
import VisitSelectWorker from '@/components/VisitSelectWorker.vue';

export default {
    components: { WideHeader, VisitTypeForm, VisitSelectDatetime, VisitSelectService, VisitSelectWorker },
    data () { 
        return { 
            // visit-type-form, visit-select- service/worker/datetime
            "current_screen": "visit-type-form",
            "worker": null,
            "services": null,
        }
    },
    methods: {
        changeCurrentScreen: function (x) { this.current_screen = x}
    }
};
</script>
