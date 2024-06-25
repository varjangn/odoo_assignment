<template>
    <div class="meeting-room-card">
      <div class="meeting-room-info">
        <h2 class="room-name">{{ roomName }}</h2>
        <p class="room-availability">{{ roomAvailability }}</p>
      </div>
      <div class="meeting-room-details">
        <div class="room-tags">
          <span v-for="(tag, index) in tags" :key="tag.id" class="tag-label">{{ tag.name }}</span>
        </div>
        <p class="seat-capacity">Seats: {{ seatCapacity }}</p>
      </div>
    </div>
  </template>

  <script>
  export default {
    name: 'MeetingRoomCard',
    props: {
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
        type: String,
        required: true
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
  }
  </style>
