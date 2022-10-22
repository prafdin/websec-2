<template>
  <template v-if="!logged">
    <header class="header-class">
      <img src="assets/alisa_logo.svg" alt="Logo" >
      <label>Alisa Control Panel</label>
      <div class="menu">
        <div style="display: flex">
          <a class="menu-item" href="panel.html">Panel</a>
          <a class="menu-item" href="settings.html">Settings</a>
        </div>

        <a class="menu-item" href="google.com">Log out</a>
      </div>
    </header>
    <br>
    <div class="forms-place">
      <p>Use yandex credentials for login</p>
      <input v-model="login" id="login-input"/>
      <input v-model="password" id="password-input" type="password" />
      <button @click="authorize">Sign in</button>
    </div>
  </template>
  <template v-else>
    <header class="header-class">
      <img src="assets/alisa_logo.svg" alt="Logo" >
      <label>Alisa Control Panel</label>
      <div class="menu">
        <div style="display: flex">
          <a class="menu-item" href="panel.html">Panel</a>
          <a class="menu-item" href="settings.html">Settings</a>
        </div>

        <a class="menu-item" href="google.com">Log out</a>
      </div>
    </header>
    <br>
    <div class="workplace">
      <div class="control-item">
        Play music
      </div>
      <div class="control-item">
        Play music by name
      </div>
    </div>
  </template>
</template>

<script>
export default {
  name: 'app',

  data () {
    return {
      logged: false,
      login: '',
      password: ''
    }
  },

  methods: {
    authorize () {
      if (this.login === '123' && this.password === '123') {
        this.logged = true
      }
    }
  }
}
</script>

<style src="./app.css"></style>
