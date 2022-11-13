<template>
  <div class="view-container">
    <div class="control-item" @click='play_music' >
      <div class="sub-control-item">
        Play music
        <img v-if="show_play_music_spinner" class="spinner-gif" src="../assets/wait_spinner.gif"  alt="loading"/>
      </div>
    </div>
    <div class="control-item" @click='stop_music'>
      <div class="sub-control-item">
        Stop music
        <img v-if="show_stop_music_spinner" class="spinner-gif" src="../assets/wait_spinner.gif"  alt="loading"/>
      </div>
    </div>
    <div class="control-item" @click="show_play_music_by_name = !show_play_music_by_name"
         :class="{ 'opened-control-item': show_play_music_by_name }">
      <div class="sub-control-item">
        Play music by name
        <img v-if="show_play_music_by_name_spinner" class="spinner-gif" src="../assets/wait_spinner.gif"  alt="loading"/>
      </div>
    </div>
    <div v-if="show_play_music_by_name" class="extended-control-item">
      <div class="interactions-place">
        <input v-model='music_name' />
        <button @click='play_music_by_name'>Play</button>
      </div>
    </div>
  </div>
</template>

<script>
import { successCodes } from '@/utils'

export default {
  data () {
    return {
      show_play_music_spinner: false,
      show_stop_music_spinner: false,
      show_play_music_by_name_spinner: false,
      show_play_music_by_name: false,
      music_name: ''
    }
  },

  methods: {
    play_music () {
      this.show_play_music_spinner = true
      fetch(
        'http://localhost:5000/play-music', {
          method: 'GET',
          credentials: 'include'
        }
      ).then(resp => {
        if (!(successCodes.includes(resp.status))) {
          this.$emit('logout_event')
        }
        this.show_play_music_spinner = false
      })
    },

    stop_music () {
      this.show_stop_music_spinner = true
      fetch(
        'http://localhost:5000/stop-music', {
          method: 'GET',
          credentials: 'include'
        }
      ).then(resp => {
        if (!(successCodes.includes(resp.status))) {
          this.$emit('logout_event')
        }
        this.show_stop_music_spinner = false
      })
    },

    play_music_by_name () {
      this.show_play_music_by_name_spinner = true
      fetch(
        'http://localhost:5000/play-music', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.music_name })
        }
      ).then(resp => {
        if (!(successCodes.includes(resp.status))) {
          this.$emit('logout_event')
        }
        this.show_play_music_by_name_spinner = false
      })

      this.music_name = ''
    }
  }
}
</script>
