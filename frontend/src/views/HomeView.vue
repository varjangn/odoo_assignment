<script>

import SearchBar from '../components/SearchBar.vue';
import MeetingRoomCard from '../components/MeetingRoomCard.vue';
import RoomDetails from '../components/RoomDetails.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    SearchBar,
    MeetingRoomCard,
    RoomDetails
  },
  data() {
    return {
      meetingRooms: [],
      selectedRoom: null,
      errMsg: '',
      renderKey: 0,
      renderKeyRoom: 0,
    };
  },
  methods: {
    async handleSearch(searchText) {
      try {
        this.selectedRoom = null;
        const token = localStorage.getItem('authToken');
        if (!token) {
          console.error('token not found');
          return []
        }
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
        const token = localStorage.getItem('authToken');
        if (!token) {
          console.error('token not found');
          return []
        }
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
      this.selectedRoom = room
      this.renderKeyRoom++
    },
    async login() {
      const data = {
        username: 'user1',
        password: 'user1@1234'
      };
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/auth/token/', data, {
            headers: {
              'Content-Type': 'application/json'
            }
        })
        if (response.status == 200) {
          const accessToken = response.data.access;
          localStorage.setItem('authToken', accessToken);
          return true;
        } else {
          this.errMsg = "Unable to login";
          return false;
        }
      } catch (error) {
        console.error('Error fetching meeting rooms:', error);
        this.errMsg = "Unable to login";
        return false;
      }
    },
    refreshComponent() {
      this.renderKey++;
    }
  },
  beforeMount() {
    this.login().then((isTokenSet) => {
      if (isTokenSet) {
        this.getRooms().then((data)=>{this.meetingRooms = data;});
      }
    });
  },
};
</script>

<template>
  <main>
    <SearchBar @search="handleSearch" />
    <div class="content">
        <div v-if="errMsg">
          {{ errMsg }}
        </div>
        <div v-else>
          <v-container class="mb-6">
            <v-row
              align="center"
              style="height: 150px;"
              no-gutters
            >
              <v-col :key="renderKey">
                <MeetingRoomCard
                  v-for="room in meetingRooms"
                  :key="room.id"
                  :roomId="room.id"
                  :roomName="room.name"
                  :roomAvailability="room.availability"
                  :tags="room.tags"
                  :seatCapacity="room.seat_capacity"
                  @click="selectRoom(room)"
                  @remove_tag_by_id="refreshComponent"
                />
              </v-col>
              <v-col>
                <div v-if="selectedRoom">
                  <RoomDetails
                    :roomId="selectedRoom.id"
                    :key="renderKeyRoom"
                    @remove_tag_by_id="refreshComponent"
                  />
                </div>
                <div v-else style="margin-left: 20px;">
                  <p>Click on a room to start booking!</p>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </div>
  </main>
</template>


<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  padding: 0;
}

.content {
  width: 100%;
  margin-top: 20px;
}

.meeting-room-container {
  width: 100%;
  padding: 10px;
}

</style>