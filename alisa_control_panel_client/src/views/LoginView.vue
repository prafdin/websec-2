<template>
  <div class="view-container">
    <div style="display: flex; justify-content: center">
      <div class="interactions-place">
        <p>Use yandex credentials for login</p>
        <input v-model="login" id="login-input"/>
        <input v-model="password" id="password-input" type="password" />
        <p v-if="showErrorMessage" class="error-message">Login or password is incorrect!</p>
        <button @click="authorize">Sign in</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from '@/router/router'
import checkLogging, { apiUrl, successCodes } from '@/utils'
export default {
  mounted () {
    this.$emit('logged', checkLogging())
  },
  data () {
    return {
      login: '',
      password: '',
      showErrorMessage: false
    }
  },
  methods: {
    async authorize () {
      const response = await fetch(
        apiUrl + `/auth?login=${this.login}&password=${this.password}`, {
          method: 'GET',
          credentials: 'include'
        }
      )

      if (successCodes.includes(response.status)) {
        this.$emit('logged', true)
        router.push('/panel')
      } else {
        this.showErrorMessage = true
      }
    }
  }
}
</script>
