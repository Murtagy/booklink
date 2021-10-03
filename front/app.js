console.log('123')

const app = Vue.createApp({
	data() {
		return { availability: { "days": [{ "date": "2021-08-18", "timeslots": [{ "time_from": "15:15:00", "time_to": "15:15:00" }] }] } }
	}
})
// {
//   data: 
// }
// )

app.mount("#app")