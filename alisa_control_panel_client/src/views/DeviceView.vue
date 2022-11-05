<template>
  <div class="device-item" >
    <img v-bind:src="device.image" alt="alternatetext">
    <p>{{ device.name }}</p>
    <input type="radio" v-bind:checked="device.used" />
  </div>
</template>

<script>
export default {
  props: ['device']
}
</script>
