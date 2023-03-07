<template>
    {{ date_parsed.format('YYYY-MM-DD') }}
    <form @submit.prevent="sumbitForm" >
    
    <label for="name">Клиент </label>
    <input id="name"/>
      
        <br>
        <label for="visittime">Время </label>
        <input id="visittime" type="time">
        <br>

    Продолжительность
    <select> 
        <option> 0 ч</option>
        <option> 1 ч</option>
        <option> 2 ч</option>
        <option> 3 ч</option>
        <option> 4 ч</option>
        <option> 5 ч</option>
        <option> 6 ч</option>
        <option> 7 ч</option>
        <option> 8 ч</option>
        <option> 9 ч</option>
    </select> 

    <select> 
        <option> 00 мин</option>
        <option> 05 мин</option>
        <option> 10 мин</option>
        <option> 15 мин</option>
        <option> 20 мин</option>
        <option> 25 мин</option>
        <option> 30 мин</option>
        <option> 35 мин</option>
        <option> 40 мин</option>
        <option> 45 мин</option>
        <option> 50 мин</option>
        <option> 55 мин</option>
    </select> 
 
    <br>
    сотрудник
    <select>
        <option v-for="worker in workers"> {{worker.name}} </option>
    </select>

    <br>
    услуги
    <select>
        <option v-for="service in services"> {{service.name}} </option>
    </select>

    </form>
</template>




<style scoped >

</style>


<script lang="ts">
import { DefaultService, type OutService, type OutWorker } from '@/client';
import dayjs from 'dayjs';


export default {
    data() {

        const services: OutService[] = []
        const workers: OutWorker[] = []

        return {
            date_parsed: dayjs(this.date),
            services: services,
            workers: workers,
        }
    },
    async mounted() {
        this.workers = (await DefaultService.getWorkers()).workers
        this.services = (await DefaultService.getServicesByUser()).services
    },
    methods: {
        submitForm() {
        
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
