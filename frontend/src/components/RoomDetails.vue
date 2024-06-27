<template>
    <div class="room-details" v-if="roomDetails" :key="renderKey">
      <div class="room-info">
        <h2 class="room-name">{{ roomDetails.name }}</h2>
        <p class="room-availability">{{ roomDetails.availability }}</p>
        <div class="room-tags" v-if="roomDetails.tags.length">
          <Tag
            v-for="tag in roomDetails.tags"
            :tagId="tag.id"
            :roomId="roomId"
            :tagName="tag.name"
            @remove_tag_by_id="removeTagById"
          />
        </div>
        <p v-else>No tags</p>
        <p class="seat-capacity">{{ roomDetails.seat_capacity }} seat capacity</p>
        <VCalendar
          :color="color" transparent borderless
          style="margin-top: 20px;"
          :attributes='attrs'
          @dayclick="changeSelectedDate"
        />
        <TimeSlot
          :bookedSlots="this.selectedDateSlots"
          :isDateSelected="this.selectedBookingDate != null"
          :key="timeSlotChangeKey"
          @time_slot_selected="childTimeSlotSelected" />

        <div v-if="this.bookingDateTimeStr || this.bookingMsg">
          <p class="booking-date" v-if="this.bookingDateTimeStr">Booking: {{ this.bookingDateTimeStr}}</p>
          <p class="success-msg" v-if="this.bookingMsg">{{this.bookingMsg}}</p>
          <p class="error-msg" v-if="this.bookingErrMsg">{{this.bookingErrMsg}}</p>
          <button class="booking-button" @click="bookRoom">Book</button>
          <button class="clear-booking-button" @click="clearBooking">Clear</button>
        </div>
      </div>
    </div>
  </template>

<script>
  import axios from 'axios';
  import Tag from '../components/Tag.vue';
  import VCalendar from 'v-calendar';
  import { ref } from 'vue';
  import TimeSlot from './TimeSlot.vue';

  export default {
    name: 'RoomDetails',
    components: {
      Tag,
      TimeSlot,
    },
    props: {
      roomId: {
        type: Number,
        required: true
      }
    },
    emits: ['remove_tag_by_id'],
    data() {
      const attrs = ref();
      return {
        roomDetails: null,
        loading: true,
        error: null,
        color: 'gray',
        renderKey: 0,
        attrs,
        bookings: [],
        selectedBookingDate: null,
        bookingDateTimeStr: '',
        bookingMsg: '',
        bookingErrMsg: '',
        selectedDateSlots: [],
        selectedTimeSlot: {},
        timeSlotChangeKey: 0,
      };
    },
    watch: {
        roomId: {
            immediate: true,
            handler(newRoomId) {
                this.fetchRoomDetails(newRoomId);
            }
        }
    },
    methods: {
      async fetchRoomDetails(roomId) {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                console.error('token not found');
                return
            }
            const response = await axios.get(`http://127.0.0.1:8000/api/room/rooms/${roomId}`, {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
            });
            const fullDayDates = []
            this.roomDetails = response.data;
            this.roomDetails.daywise_bookings.forEach(entry => {
                if (entry.slots.length >= 16) {
                  entry.isFullyOccupied = true
                  fullDayDates.push(new Date(entry.date))
                } else {
                  entry.isFullyOccupied = false
                }
                if (new Date(entry.date).toDateString() === new Date().toDateString()) {
                  this.selectedDateSlots = JSON.parse(JSON.stringify(entry.slots))
                }
            });
            this.bookings = JSON.parse(JSON.stringify(this.roomDetails.daywise_bookings))
            this.attrs = [
              {
                content: 'red',
                dates: fullDayDates,
              },
              {
                key: 'today',
                dot: true,
                dates: new Date(),
              },
            ]
        } catch (error) {
            this.error = 'Error fetching room details';
            console.error('Error fetching room details:', error);
        } finally {
            this.loading = false;
        }
      },
      removeTagById(payload) {
        for (let i = 0; i < this.roomDetails.tags.length; i++) {
          let tag = this.roomDetails.tags[i]
          if (tag.id === payload) {
            this.roomDetails.tags.splice(i, 1);
            this.$emit('remove_tag_by_id', i);
          }
        }
      },
      changeSelectedDate(dateObj) {
        this.selectedBookingDate = dateObj.date
        this.timeSlotChangeKey++
        let slots = []
        for (let i = 0; i < this.bookings.length; i++) {
          let booking = this.bookings[i]
          if (new Date(booking.date).toDateString() === dateObj.date.toDateString()) {
            slots = booking.slots
            break
          }
        }
        this.selectedDateSlots = slots
      },
      childTimeSlotSelected(payload) {
        this.selectedTimeSlot = JSON.parse(JSON.stringify(payload))
        if (this.selectedBookingDate) {
          const year = this.selectedBookingDate.getFullYear();
          const month = String(this.selectedBookingDate.getMonth() + 1).padStart(2, '0');
          const day = String(this.selectedBookingDate.getDate()).padStart(2, '0');
          const slot = `${this.selectedTimeSlot.start} - ${this.selectedTimeSlot.end}`
          this.bookingDateTimeStr = `${year}-${month}-${day} ${slot}`;
        }
      },
      async bookRoom() {
        if (!this.selectedBookingDate || !this.selectedTimeSlot) {
          console.log('booking not selected')
          return
        }

        const token = localStorage.getItem('authToken');
        if (!token) {
          console.error('token not found');
          return false
        }

        try {
            const year = this.selectedBookingDate.getFullYear();
            const month = String(this.selectedBookingDate.getMonth() + 1).padStart(2, '0');
            const day = String(this.selectedBookingDate.getDate()).padStart(2, '0');
            const bookingDateStr = `${year}-${month}-${day}`
            const data = {
              room_id: this.roomId,
              date: bookingDateStr,
              timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
              slots: [this.selectedTimeSlot.slotStr]
            }
            const response = await axios.post(`http://127.0.0.1:8000/api/room/add-booking/`, data, {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              }
            })
            if (response.status == 201) {
              this.bookingMsg = 'Booking successfull!'
              this.bookingErrMsg = ''
              await this.fetchRoomDetails(this.roomId)
              this.clearBooking()
            } else {
              this.bookingMsg = ''
              this.bookingErrMsg = response.data.detail
            }
        }
        catch (error) {
            if (error.response.status == 406) {
              this.bookingMsg = ''
              this.bookingErrMsg = error.response.data.detail
            } else {
              console.error('Error deleting tags:', error);
            }
            return false;
        }
      },
      clearBooking() {
        this.selectedBookingDate = null
        this.selectedTimeSlot = {}
        this.bookingDateTimeStr = ''
        this.renderKey++
      }
    }
  };
  </script>

  <style scoped>
  .room-details {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 10px;
    width: 100%;
  }

  .room-info {
    margin-top: 5px;
  }

  .room-name {
    margin: 0;
    font-size: 1.5em;
  }

  .room-availability {
    margin: 0;
    color: #888;
  }

  .room-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 10px;
  }

  .tag-label {
    background-color: #e0e0e0;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 0.9em;
    color: #333;
  }

  .seat-capacity {
    margin-top: 10px;
  }
  .booking-date {
    margin: 5px;
    padding-left: 5px;
  }
  .success-msg {
    color: green;
  }
  .error-msg {
    color: #f79393;
  }
  .booking-button {
    margin: 5px;
    padding: 10px 20px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 10px 10px 10px 10px;
    background-color: #000000;
    color: #fff;
    cursor: pointer;
    outline: none;
  }
  .clear-booking-button {
    margin: 5px;
    padding: 10px 20px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 10px 10px 10px 10px;
    background-color: #f79393;
    color: #fff;
    cursor: pointer;
    outline: none;
  }
  </style>
