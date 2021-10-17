<template>
    <div v-if="user">
        My user: {{user}}
    </div>
</template>

<script>
export default {
    data() {return {'user': null}},
    methods: {
        getUser() {
            console.log('Getting user for jwt', this.$store.state.jwt_auth)
            this.$api.get('/my_user', {"headers" :{'Authorization': 'bearer ' + this.$store.state.jwt_auth}})
            .then(response => { if (response.data==null) {alert('Not logged in')} else {let user_id = response.data.user_id; console.log('GOT USER', response); this.user = user_id;  }})
        }
    },
    created() {
        console.log('CREATED')
        this.getUser()
    }
}
</script>