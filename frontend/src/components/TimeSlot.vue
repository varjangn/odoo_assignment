<template>
    <div class="time-slots">
      <button
        v-for="(slot, index) in slots"
        :key="index"
        @click="selectSlot(index)"
        :class="{
          'selected': selectedSlotIndex === index,
          'booked': slot.isBooked === true,
          'cursor-not-allowed': !this.isDateSelected,
        }"
      >
        {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
      </button>
    </div>
  </template>

  <script>
  export default {
    props: {
      bookedSlots: {
        type: Array,
        required: true
      },
      isDateSelected: {
        type: Boolean,
        required: true
      },
    },
    data() {
      return {
        startTime: "10:00",
        endTime: "21:00", // TODO
        duration: 30,
        slots: [],
        selectedSlotIndex: -1
      };
    },
    emits: {
      time_slot_selected: null
    },
    mounted() {
      this.updateSlots();
    },
    methods: {
      updateSlots() {
        let start = this.startTime;
        let end = this.endTime;
        let duration = this.duration;

        this.slots = [];
        let currentTime = start;

        while (this.compareTime(currentTime, end) < 0) {
          let nextTime = this.addMinutes(currentTime, duration);
          if (this.compareTime(nextTime, end) > 0) {
            nextTime = end;
          }

          const currSlotStr = `${currentTime}~${nextTime}`;
          let isBooked = false;
          for (let i = 0; i < this.bookedSlots.length; i++) {
            const slotStr = this.bookedSlots[i]
            if (slotStr === currSlotStr) {
              isBooked = true
              break
            }
          }

          this.slots.push({
            start: currentTime,
            end: nextTime,
            isBooked,
            slotStr: currSlotStr,
          });

          currentTime = nextTime;
        }
      },
      addMinutes(time, minsToAdd) {
        let [hours, minutes] = time.split(":").map(Number);
        minutes += minsToAdd;

        while (minutes >= 60) {
          minutes -= 60;
          hours += 1;
        }

        hours = hours.toString().padStart(2, "0");
        minutes = minutes.toString().padStart(2, "0");

        return `${hours}:${minutes}`;
      },
      compareTime(t1, t2) {
        const [h1, m1] = t1.split(":").map(Number);
        const [h2, m2] = t2.split(":").map(Number);

        if (h1 < h2 || (h1 === h2 && m1 < m2)) {
          return -1;
        } else if (h1 > h2 || (h1 === h2 && m1 > m2)) {
          return 1;
        }
        return 0;
      },
      formatTime(time) {
        return time;
      },
      selectSlot(index) {
        this.selectedSlotIndex = index;
        const slot = this.slots[index]
        this.$emit('time_slot_selected', slot);
      },
    },
  };
  </script>

  <style scoped>
  .time-slots {
    display: flex;
    flex-wrap: wrap;
  }
  .time-slots button {
    background-color: #e0e0e0;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 0.9em;
    color: #333;
    margin: 5px;
  }
  .time-slots button.selected {
    background-color: #475569;
    color:  #e0e0e0;;
  }
  .time-slots button.booked {
    color:  #dc2626;
    cursor: not-allowed;
    font-weight: bold;
  }
  .cursor-not-allowed {
    cursor: not-allowed;
  }
  </style>
