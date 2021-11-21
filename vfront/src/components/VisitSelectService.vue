<template>
  <div v-if="services"> 
    <form>
        <ul>
        <li class="button">
            <button>Далее <img src="../assets/arrow.png"></button>
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

export default {
    components: { },
    data () { 
        return { 
            services: [ // test data for now
                {"name": "Услуга X", "price": 25, "currency": "бел.руб", "id": "some_id1"}, 
                {"name": "Услуга Y", "price": 25, "currency": "бел.руб", "id": "some_id2"},
                {"name": "Услуга Z", "price": 25, "currency": "бел.руб", "id": "some_id3"},
                {"name": "Услуга A", "price": 25, "currency": "бел.руб", "id": "some_id4"}, 
                {"name": "Услуга B", "price": 25, "currency": "бел.руб", "id": "some_id5"},
                {"name": "Услуга C", "price": 25, "currency": "бел.руб", "id": "some_id6"},
            ],
            checkedServices: [],
        }
    },
    methods: {
        changeCurrentScreen: function (x) { this.current_screen = x}
    }
};

</script>
