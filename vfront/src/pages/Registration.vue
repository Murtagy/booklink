<template>
<div>
<wide-header title="Регистрация"></wide-header>
<form>
    <ul>
        <li>
            <label for="company">Компания</label>
            <input type="text" v-model="company" id="company" placeholder="Введите наименование юр. лица" required>
        </li>
        <li>
            <label for="email">E-mail</label>
            <input type="email" v-model="email" id="email" placeholder="Введите адрес электронной почты" required>
        </li>
        <li>
            <label for="username">Логин</label>
            <input type="text" v-model="username" id="username" placeholder="Введите имя пользователя" required>
        </li>
        <li>
            <label for="password">Пароль</label>
            <input type="password" v-model="password" id="password" placeholder="Введите пароль" required>
        </li>
        <li>
            <label for="password-confirmation">Подтвердите пароль</label>
            <input type="password" v-model="password_confirmation" id="password-confirmation" placeholder="Введите пароль" required>
        </li>
        <input type="submit" value="Создать пользователя" name="submit" id="submit">
    </ul>
    
</form>
</div>
</template>

<script>
import WideHeader from '../components/WideHeader.vue'
export default {
  components: { WideHeader },
    data () { 
        return {
            'email': '',
            'company': '',
            'username': '',
            'password': '',
            'password_confirmation': '',

        }
    }
}
</script>

