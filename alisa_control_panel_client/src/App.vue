<template>
  <header class="header-class">
    <img src="../public/alisa_logo.svg" alt="Logo" >
    <label>Alisa Control Panel</label>
    <div class="menu">
      <div style="display: flex">
       <a><router-link class="menu-item" to="/panel"  >Panel</router-link></a>
       <a><router-link class="menu-item" to="/settings" >Settings</router-link></a>
      </div>
      <a v-show="logged" @click="logout" class="menu-item">Log out</a>
    </div>
  </header>
  <br>
  <router-view v-on:logged="(logging_status) => this.logged = logging_status" />
</template>

<script>
import checkLogging from '@/utils'

export default {
  name: 'app',

  mounted () {
    this.logged = checkLogging()
  },

  data () {
    return {
      logged: false
    }
  },

  methods: {
    async logout () {
      await fetch(
        'http://localhost:5000/logout', {
          method: 'GET',
          credentials: 'include'
        }
      )
      this.$router.push('/login')
    }
  }
}
</script>
