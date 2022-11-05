<template>
  <div class="workplace">
    <div class="control-item" @click="change_device_view = !change_device_view"
         :style="!change_device_view ? {'margin': '0 0 30px'} : {'margin': '0 0 0px'}">
      Change device
    </div>
    <div v-if="change_device_view" class="open-control-item">
      <div class="forms-place">
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

export default {
  components: {
    DeviceView
  },

  async mounted () {
    const response = await fetch(
      'http://localhost:5000/get-devices', {
        method: 'GET',
        credentials: 'include'
      }
    )
    const successCodes = [200]

    if (successCodes.includes(response.status)) {
      this.devices = await response.json()
      console.log(this.devices)
    } else {
      this.devices = []
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
        'http://localhost:5000/change-device', {
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
