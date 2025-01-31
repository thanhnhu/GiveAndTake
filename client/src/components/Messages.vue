<template>
  <div class="hello">
    <img src='@/assets/logo-django.png' style="width: 250px" />
    <p>The data below is added/removed from the SQLite Database using Django's ORM and Rest Framework.</p>
    <br/>
    <p>Subject</p>
    <input type="text" placeholder="Hello" v-model="subject">
    <p>Message</p>
    <input type="text" placeholder="From the other side" v-model="msgBody">
    <br><br>
    <input 
      type="submit" 
      value="Add" 
      @click="addMessage({ subject: subject, body: msgBody })" 
      :disabled="!subject || !msgBody">

    <hr/>
    <h3>Messages on Database</h3>
    <p v-if="messages.length === 0">No Messages</p>
    <div class="msg" v-for="(msg, index) in messages" :key="msg.pk">
        <p class="msg-index">[{{index}}]</p>
        <p class="msg-subject" v-html="msg.subject"></p>
        <p class="msg-body" v-html="msg.body"></p>
        <input type="submit" @click="deleteMessage(msg.pk)" value="Delete" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { messagesStoreObj } from '@/stores/messages'

const messagesStore = messagesStoreObj()
const subject = ref("")
const msgBody = ref("")

const messages = computed(() => messagesStore.messages)

const addMessage = (message) => {
  messagesStore.addMessage(message)
}

const deleteMessage = (pk) => {
  messagesStore.deleteMessage(pk)
}

// Load messages when component is created
onMounted(() => {
  messagesStore.getMessages()
})
</script>

<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>
