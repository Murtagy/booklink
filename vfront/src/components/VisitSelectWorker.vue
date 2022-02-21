<template>
    <div id="main">
        <button 
            v-for="worker in workers" :key="worker.worker_id" 
            @click="emitWorker(worker)">
            <img src="../assets/worker-photo.jpg">
            <span id="name">{{ worker.name }} </span>
            <br><br><span id="job">{{ worker.job_title }}</span><br>
            <br>{{ worker.description }} </button>
    </div>
</template>

<style scoped src="@/assets/styles/worker.css"></style>

<script>

export default {
    components: { },
    data () { return {} 
    },
    methods: {
        emitWorker: function (x) { 
            this.$emit('select-worker', x);
            this.$emit('go-start-screen'); 
        }
    },
    props: ["workers"],
};


</script>
