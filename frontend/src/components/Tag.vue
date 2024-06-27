<template>
    <span class="tag-label">{{ tagName }}</span>
    <button class="tag-close-button" @click="removeTag(tagId, roomId)">✖</button>
</template>

<script>
import axios from 'axios';
export default {
name: 'Tag',
props: {
    tagId: {
        type: Number,
        required: true
    },
    tagName: {
        type: String,
        required: true
    },
    roomId: {
        type: Number,
        required: true
    }
},
emits: {
    remove_tag_by_id: null
},
async mounted() {},
methods: {
    async removeTag(tagId, roomId) {
        const token = localStorage.getItem('authToken');
        if (!token) {
          console.error('token not found');
          return []
        }
        try {
            const data = {
                tag_ids: [tagId]
            }
            const response = await axios.post(`http://127.0.0.1:8000/api/room/rooms/${roomId}/remove_tags/`, data, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            const success = response.data?.success
            if (success) {
                this.$emit('remove_tag_by_id', tagId);
            }
            return response.data?.success;
        }
        catch (error) {
            console.error('Error deleting tags:', error);
            return false;
        }
    }
}
};
</script>

<style scoped>
.tag-label {
    background-color: #e0e0e0;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 0.9em;
    color: #333;
}
.tag-close-button {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 0.8em;
    margin-left: 5px;
    padding: 0;
    position: relative;
    top: -9px;
    right: -5px;
    left: -10px;
}
</style>
