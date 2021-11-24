<template>
    <div id="main">
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
        <button @click="emitWorker({'name': 'Анастасия Кoвалёва'})"><img src="../assets/worker-photo.jpg"><span id="name">Анастасия Кoвалёва</span><br><br><span id="job">Мастер-бровист</span><br><br>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Et, esse sunt qui quis saepe neque, ea impedit laborum illum, dolores error nobis natus doloremque cumque nemo! Neque quisquam nemo unde. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Error eum odio cupiditate officiis laboriosam quibusdam quod sint, illo praesentium adipisci atque suscipit consectetur in nesciunt quasi quas explicabo earum mollitia?</button>
    </div>
</template>

<style scoped src="@/assets/styles/worker.css"></style>

<script>

export default {
    components: { },
    data () { 
        return { 
            workers: [ //  TODO test data
            ],
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
