<template>

</template>

<script lang="ts">
import VisitsDay from "@/components/VisitsDay.vue"


export default {
    components: {VisitsDay},
    computed: {
        date() {
            return this.$route.params.date
        },
    },
    // mounted(): {
        // this.fetchVisit
    // }
}
</script>