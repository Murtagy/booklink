<template>
  <div 
    v-on:visit-select="changeCurrentScreen" 
  >
    <wide-header title="Онлайн-запись" />
    <visit-type-form 
        v-on:visit-select="changeCurrentScreen" 
        v-if="current_screen=='visit-type-form'"
    />
    <p v-if="current_screen== 'visit-select-service'"> Selecting service  </p>
    <p v-if="current_screen==  'visit-select-worker'"> Selecting worker   </p>
    <p v-if="current_screen=='visit-select-datetime'"> Selecting datetime </p>
  </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import WideHeader from "@/components/WideHeader.vue";
import VisitTypeForm from "@/components/VisitTypeForm.vue"

export default {
    components: { WideHeader, VisitTypeForm },
    data () { 
        return { 
            // visit-type-form, visit-select- service/worker/datetime
            "current_screen": "visit-type-form" 
        }
    },
    methods: {
        changeCurrentScreen: function (x) { this.current_screen = x}
    }
};
</script>
