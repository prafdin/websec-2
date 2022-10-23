<template>
  <header class="header-class">
    <img src="assets/alisa_logo.svg" alt="Logo" >
    <label>Alisa Control Panel</label>
    <div class="menu">
      <div style="display: flex">
       <a><router-link class="menu-item" to="/panel"  >Panel</router-link></a>
       <a><router-link class="menu-item" to="/settings" >Settings</router-link></a>
      </div>
      <a v-show="logged" class="menu-item" href="google.com">Log out</a>
    </div>
  </header>
  <br>
  <router-view/>
</template>

<script>
export default {
  name: 'app',

  data () {
    return {
      logged: true
    }
  }
}
</script>

<style src="./app.css"></style>
