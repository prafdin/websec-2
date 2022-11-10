<template>
  <div class="view-container">
    <div class="control-item" @click='play_music' >
      Play music
    </div>
    <div class="control-item" @click='stop_music'>
      Stop music
    </div>
    <div class="control-item" @click="show_play_music_by_name = !show_play_music_by_name"
         :class="{ 'opened-control-item': show_play_music_by_name }">
      Play music by name
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
export default {
  data () {
    return {
      show_play_music_by_name: false,
      music_name: ''
    }
  },

  methods: {
    play_music () {
      fetch(
        'http://localhost:5000/play-music', {
          method: 'GET',
          credentials: 'include'
        }
      )
    },

    stop_music () {
      fetch(
        'http://localhost:5000/stop-music', {
          method: 'GET',
          credentials: 'include'
        }
      )
    },

    play_music_by_name () {
      fetch(
        'http://localhost:5000/play-music', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.music_name })
        }
      )

      this.music_name = ''
    }
  }
}
</script>
