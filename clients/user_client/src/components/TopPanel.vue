<template>
  <div class="topnav">
    <input type="checkbox" id="menu" />
    <label id="menu_label" class="menu; sized" for="menu" style="float: left"
      ><img src="@/assets/menu.svg" style="height: 10px"
    /></label>
    <div class="menu-content">
      <router-link to="/visits">
        <a class="sized">Визиты</a>
      </router-link>

      <router-link to="/vcalendar">
        <a class="sized">Календарь</a>
      </router-link>

      <router-link to="/workers">
        <a class="sized">Юниты</a>
      </router-link>

      <router-link to="/services">
        <a class="sized">Услуги</a>
      </router-link>

      <router-link to="/my_user" style="position: absolute; right: 0">
        <img
          src="@/assets/worker-icon.png"
          style="height: 35px; width: 35px; margin-top: 5px"
        />
      </router-link>
    </div>
  </div>
</template>

<style scoped css>
.topnav {
  overflow: hidden;
  background-color: var(--color3);
  position: relative;
  display: flex;
  flex-direction: row;
}

.topnav .sized {
  font-size: 17px;
  float: left;
  padding: 14px 16px;
}

.topnav a {
  text-decoration: none;
  color: white;
}

.topnav label {
  float: left;
  background-color: var(--color2);
  color: white;
}
.topnav label:hover {
  background-color: #ddd;
}
.topnav a.icon {
  float: right;
}

.topnav a:hover {
  background-color: #ddd;
  color: black;
}

.topnav input#menu {
  display: none;
}

.menu-content {
  float: left;
  max-height: 0;
  overflow: hidden;
  /* width: calc(100% - 35px)   */
  /* 35 px - icon size */
}
/* Toggle Effect */
input:checked ~ .menu-content {
  max-height: 1000px;
  transition: all ease 1s;
}
input:checked ~ label {
  background: url(img/open.png) no-repeat left center;
}
</style>
