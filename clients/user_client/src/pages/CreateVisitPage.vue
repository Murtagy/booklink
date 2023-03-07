<template>
    {{ date_parsed }}
</template>




<style scoped >

</style>


<script lang="ts">
import dayjs from 'dayjs';


export default {
    data() {
        return {
            date_parsed: dayjs(this.date)
        }
    },
    props: {
        date: {
            type: String,
            required: true
        }
    }
}
</script>
