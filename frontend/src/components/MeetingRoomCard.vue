<template>
    <div class="meeting-room-card">
      <div class="meeting-room-info">
        <h2 class="room-name">{{ roomName }}</h2>
        <p class="room-availability">{{ roomAvailability }}</p>
      </div>
      <div class="meeting-room-details">
        <div class="room-tags" v-if="tags.length">
          <Tag
            v-for="tag in tags"
            :tagId="tag.id"
            :tagName="tag.name"
            :roomId="roomId"
            @remove_tag_by_id="removeTagById"
          />
        </div>
        <p v-else>No tags</p>
        <p class="seat-capacity">{{ seatCapacity }} seat capacity</p>
      </div>
    </div>
  </template>

  <script>
  import Tag from '../components/Tag.vue';
  export default {
    name: 'MeetingRoomCard',
    components: {
      Tag,
    },
    props: {
      roomId: {
        type: Number,
        required: true,
      },
      roomName: {
        type: String,
        required: true
      },
      roomAvailability: {
        type: String,
        required: true
      },
      tags: {
        type: Array,
        required: true
      },
      seatCapacity: {
        type: Number,
        required: true
      }
    },
    methods:{
      removeTagById(payload) {
        for (let i = 0; i < this.tags.length; i++) {
          let tag = this.tags[i]
          if (tag.id === payload) {
            this.tags.splice(i, 1);
            this.$emit('remove_tag_by_id', i);
            break
          }
        }
      }
    }
  }
  </script>

  <style scoped>
  .meeting-room-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 10px 0;
  }

  .meeting-room-info {
    flex: 1;
  }

  .room-name {
    margin: 0;
    cursor: pointer;
    font-size: 1.5em;
  }

  .room-availability {
    margin: 0;
    color: #888;
  }

  .meeting-room-details {
    flex: 1;
    text-align: right;
  }

  .room-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }

  .tag-label {
    background-color: #e0e0e0;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 0.9em;
    color: #333;
  }

  .seat-capacity {
    margin: 0;
    margin-top: 10px;
  }
  </style>
