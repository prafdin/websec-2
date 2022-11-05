<template>
  <div class="workplace">
    <div class="control-item" :style="{'margin': '0 0 30px'}" >
      Play music
    </div>
    <div class="control-item" :style="{'margin': '0 0 30px'}" >
      Stop music
    </div>
    <div class="control-item" @click="show_play_music_by_name = !show_play_music_by_name">
      Play music by name
    </div>
    <div v-if="show_play_music_by_name" class="open-control-item">
      <div class="forms-place">
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
    async play_music_by_name () {
      fetch(
        'http://localhost:5000/play-by-name', {
          method: 'POST',
          credentials: 'include',
          body: JSON.stringify({ name: this.music_name })
        }
      )

      this.music_name = ''
    }

  }
}
</script>
