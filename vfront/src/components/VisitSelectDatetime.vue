<template>    
    <div> 
        <calendar
            v-bind:availability=availability
            v-bind:availability_mode=availability_mode
        />
    </div>
</template>

<style scoped src="@/assets/styles/visit.css"></style>

<script>
import Calendar from "@/pages/Calendar"

export default {
  components: { Calendar },
    data() { 
        return {
            "availability_mode": true
        } 
    },
    props: ['availability'],

}

</script>
