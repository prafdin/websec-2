<template>
  <div class="forms-place">
    <p>Use yandex credentials for login</p>
    <input v-model="login" id="login-input"/>
    <input v-model="password" id="password-input" type="password" />
    <button @click="authorize">Sign in</button>
  </div>
</template>

<script>
import router from '@/router/router'

export default {
  mounted () {
    this.$emit('logged', false)
  },
  data () {
    return {
      login: '',
      password: ''
    }
  },
  methods: {
    async authorize () {
      const r = await fetch(
        `http://localhost:5000/auth?login=${this.login}&password=${this.password}`, {
          method: 'GET',
          credentials: 'include'
        }
      )

      this.$emit('logged', true)
      console.log(r)

      router.push('/panel')
    }
  }
}
</script>
