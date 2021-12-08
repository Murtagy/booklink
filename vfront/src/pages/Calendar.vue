<template>
  <div class="main">
    <wide-header title="Выбор даты"></wide-header>
    <button class="left">
      <img class="left" src="../assets/arrow2.png" />
    </button>
    <div class="month">Ноябрь 2021</div>
    <button class="right">
      <img class="right" src="../assets/arrow2.png" />
    </button>
    <div class="dates">
      <span class="clickable">1</span><span>2</span><span>3</span
      ><span class="clickable">4</span><span class="clickable">5</span
      ><span>6</span><span>7</span><span>8</span><span>9</span
      ><span class="clickable">10</span><span class="clickable">11</span
      ><span>12</span><span class="clickable">13</span><span>14</span
      ><span>15</span><span>16</span><span>17</span
      ><span class="clickable">18</span><span class="clickable">19</span
      ><span>20</span><span class="clickable">21</span
      ><span class="clickable">22</span><span class="clickable">23</span
      ><span>24</span><span>25</span><span>26</span><span>27</span
      ><span class="clickable">28</span><span class="clickable">29</span
      ><span>30</span><span class="empty"></span><span class="empty"></span
      ><span class="empty"></span><span class="empty"></span
      ><span class="empty"></span>
    </div>
    <br />
    <div class="explication">
      <span class="square clickable"></span>
      <span class="description">- дата доступна для выбора</span>
      <br /><br />
      <span class="square"></span>
      <span class="description">- дата не доступна для выбора</span>
    </div>
  </div>
</template>

<script>
import WideHeader from "../components/WideHeader.vue";
export default {
  data() {
    return {};
  },
  methods: {},
  components: { WideHeader },
};
</script>
<style scoped src="@/assets/styles/calendar.css"></style>
