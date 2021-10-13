<template>
<div>
<header>
	<h1>Регистрация</h1>
</header>
<br>

<form>
    <ul>
        <li>
            <label for="company">Компания</label>
            <input type="text" name="company" id="company" placeholder="Введите наименование юр.лица" required>
        </li>
        <li>
            <label for="email">E-mail</label>
            <input type="email" name="email" id="email" placeholder="Введите адрес электронной почты" required>
        </li>
        <li>
            <label for="username">Логин</label>
            <input type="text" name="username" id="username" placeholder="Введите имя пользователя" required>
        </li>
        <li>
            <label for="password">Пароль</label>
            <input type="password" name="password" id="password" placeholder="Введите пароль" required>
        </li>
        <li>
            <label for="password-confirmation">Подтвердите пароль</label>
            <input type="password" name="password-confirmation" id="password-confirmation" placeholder="Введите пароль" required>
        </li>
        <input type="submit" value="Создать пользователя" name="submit" id="submit">
    </ul>
    
</form>
</div>
</template>
