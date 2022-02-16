<template>
  <div v-if="services"> 
    <form>
    <ul>
    <li class="button">
        <button @click="emitServices">Далее <img src="../assets/arrow.png"></button>
    </li>
    {{checkedServices}}
    <li v-for="service in services" :key="service.name">
        <input type="checkbox" class="checkbox" name="service" :id="service.id" :value="service" v-model="checkedServices">
        <label :for="service.id">{{service.name}}</label>
        <span class="price">{{service.price}} {{service.currency}}</span>
    </li>
    </ul>   
    </form>    
  </div>
</template>

<style scoped src="@/assets/styles/services.css"></style>

<script>
import services_mock from "@/mocks/services_mock.js"

export default {
    components: { },
    data () { 
        if (process.env.VUE_APP_OFFLINE) {
            return { 
                services: services_mock["mock"],
                checkedServices: [],
            }
        }
        // TODO get services in online mode

    },
    methods: {
        emitServices: function () { 
            this.$emit('check-services', this.checkedServices);
            this.$emit('go-start-screen'); 
            console.log(this.checkedServices)
        }
    }
};

</script>
