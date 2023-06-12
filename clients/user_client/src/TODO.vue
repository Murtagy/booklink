<template>
  <div>
    <span
      class="todo-icon"
      @click="show = !show"
    >
      <i class="fas fa-tasks"></i>
    </span>
    <div  v-if="show" style="color: orange">
      <slot> </slot>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      show: false,
    }
  }
}
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

.todo-icon {
  position: sticky;
  top: 10px;
  right: 10px;
  color: orange;
  cursor: pointer;
}
.todo-list {
  margin-top: 20px;
}
</style>
