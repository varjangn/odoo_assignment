<script>

import SearchBar from '../components/SearchBar.vue';
import MeetingRoomCard from '../components/MeetingRoomCard.vue';
import axios from 'axios';


export default {
  name: 'App',
  components: {
    SearchBar,
    MeetingRoomCard
  },
  data() {
    return {
      meetingRooms: [],
      selectedRoom: null,
    };
  },
  methods: {
    async handleSearch(searchText) {
      try {
        const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MzExOTY3LCJpYXQiOjE3MTkzMTE2NjcsImp0aSI6IjI4NTBlMGNiODMxNDQxNGZiNWM0ZjA4YWQyNzQxMDFmIiwidXNlcl9pZCI6Mn0.cbE899eCfGkyML-8OG6ch5Yrdd48AkhX18tdAyKg9C0';
        const resp = await axios.get(`http://127.0.0.1:8000/api/room/rooms/?search=${searchText}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = resp.data;
        if (resp.status == 200) {
          this.meetingRooms = data;
        } else {
          this.meetingRooms = [];
        }
      } catch (error) {
        console.error('Error fetching meeting rooms:', error);
        this.meetingRooms = []
      }
    },
    async getRooms() {
      try {
        const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5MzExOTY3LCJpYXQiOjE3MTkzMTE2NjcsImp0aSI6IjI4NTBlMGNiODMxNDQxNGZiNWM0ZjA4YWQyNzQxMDFmIiwidXNlcl9pZCI6Mn0.cbE899eCfGkyML-8OG6ch5Yrdd48AkhX18tdAyKg9C0';
        const resp = await axios.get("http://127.0.0.1:8000/api/room/rooms/", {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = resp.data;
        if (resp.status == 200) {
          return data;
        }
        return []
      } catch (error) {
        console.error('Error fetching meeting rooms:', error);
        return []
      }
    },
    selectRoom(room) {
      this.selectedRoom = room;
    },
  },
  beforeMount() {
    this.getRooms().then((data) => {this.meetingRooms = data;});
  },
};
</script>

<template>
  <main>
    <SearchBar @search="handleSearch" />
    <div class="content">
      <div class="meeting-room-container">
        <MeetingRoomCard
          v-for="room in meetingRooms"
          :key="room.id"
          :roomName="room.name"
          :roomAvailability="room.availability"
          :tags="room.tags"
          :seatCapacity="room.seat_capacity"
          @click="selectRoom(room)"
        />
      </div>
    </div>
  </main>
</template>


<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  flex-direction: column;
}

.content {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin-top: 20px;
}

.meeting-room-container {
  width: 100%;
  padding: 10px;
}

.meeting-room-container {
  max-width: 100%;
}

</style>