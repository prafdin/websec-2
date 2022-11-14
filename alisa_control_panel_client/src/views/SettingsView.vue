<template>
  <div class="view-container">
      <div class="control-item" @click="change_device_view = !change_device_view"
           :class="{ 'opened-control-item': change_device_view }">
        Change device
      </div>
      <div v-if="change_device_view" class="extended-control-item">
        <div class="interactions-place">
          <device-view
            v-for="d in devices"
            :key="d"
            v-bind:device="d"
            @click="change_device(d)">
          </device-view>
        </div>
      </div>
  </div>
</template>

<script>
import DeviceView from './DeviceView'
import { apiUrl, successCodes } from '@/utils'

export default {
  components: {
    DeviceView
  },

  async mounted () {
    const response = await fetch(
      apiUrl + '/get-speakers', {
        method: 'GET',
        credentials: 'include'
      }
    )

    if (!(successCodes.includes(response.status))) {
      this.$emit('logout_event')
    } else {
      this.devices = await response.json()
    }
  },

  data () {
    return {
      change_device_view: false,
      devices: []
    }
  },

  methods: {
    change_device (device) {
      fetch(
        apiUrl + '/change-device', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(device)
        }
      )
        .then((res) => {
          return res.json()
        })
        .then((devices) => {
          this.devices = devices
        })
    }
  }
}
</script>
