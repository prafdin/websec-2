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
import checkLogging from '@/utils'
export default {
  mounted () {
    this.$emit('logged', checkLogging())
  },
  data () {
    return {
      login: '',
      password: ''
    }
  },
  methods: {
    async authorize () {
      const response = await fetch(
        `http://localhost:5000/auth?login=${this.login}&password=${this.password}`, {
          method: 'GET',
          credentials: 'include'
        }
      )

      const successCodes = [200]

      console.log(response.status)

      if (successCodes.includes(response.status)) {
        this.$emit('logged', true)
        router.push('/panel')
      }
    }
  }
}
</script>
