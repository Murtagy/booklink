<template>
    <div id="main">
        <button 
            v-for="worker in workers" :key="worker.id" 
            @click="emitWorker({'name': worker.name})">
            <img src="../assets/worker-photo.jpg">
            <span id="name">{{ worker.name }} </span>
            <br><br><span id="job">{{ worker.job_title }}</span><br>
            <br>{{ worker.description }} </button>
    </div>
</template>

<style scoped src="@/assets/styles/worker.css"></style>

<script>

import workers_mock from "@/mocks/workers_mock.js"

export default {
    components: { },
    data () { 
        if (process.env.VUE_APP_OFFLINE) {
        return { 
            workers: workers_mock["mock"],
        }
        }
    },
    methods: {
        emitWorker: function (x) { 
            this.$emit('select-worker', x);
            this.$emit('go-start-screen'); 
            console.log(this.checkedServices)
        }
    }
};


</script>
