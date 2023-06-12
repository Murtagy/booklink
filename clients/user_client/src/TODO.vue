<template>
  <div>
    <span
      class="todo-icon"
      @click="show = !show"
    >
      <i class="fas fa-tasks"></i>
    </span>
    <ul v-if="show" class="todo-list">
        {{ todos }}
    </ul>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    todos: {
      type: String,
      required: true
    }
  },
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
  position: absolute;
  top: 10px;
  right: 10px;
  color: orange;
  cursor: pointer;
}
.todo-list {
  margin-top: 20px;
}
</style>
