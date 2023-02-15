<template>
  <header>
    <!-- <img id="our_logo" src="../assets/logo.png" /> -->
    <h1>{{ title }}</h1>
    <hr class="line1" />
    <hr class="line2" />
    <hr class="line3" />
  </header>
</template>

<style scoped>
  header {
    max-width: 100%;
    background-color: var(--color3);
    position: sticky;
    margin-left: 20px;
    margin-right: 20px;
    border-radius: 5px;
  }

  header h1 {
    font-family: "TimesNewRoman";
    color: white;
    text-align: center;
    /* margin-top: 40px; */
    margin-bottom: 15px;
    text-shadow: 1px 2px var(--color1);
  }

  header img#our_logo {
    position: absolute;
    left: 0;
    top: 0;
    width: 7em;
    height: 3em;
  }

  header hr.line1 {
    background-color: white;
    height: 7px;
    margin: 0;
    border: none;
  }

  header hr.line2 {
    background-color: var(--color1);
    height: 3px;
    margin: 0;
    border: none;
  }


  @media screen and (max-width: 900px) {
    header h1 {
      padding: 30px auto;
      font-size: 40px;
    }

    header img {
      width: 8em;
      height: 5em;
    }
  }

  @media screen and (max-width: 620px) {
    header h1 {
      font-size: 30px;
    }

    header img {
      width: 7em;
      height: 4em;
    }

  }

  @media screen and (max-width: 450px) {
    header h1 {
      font-size: 2em;
    }

    header img {
      width: 5em;
      height: 3em;
    }
}
</style>

<script lang="ts">
export default {
  props: {
    title: String,
  },
};
</script>
