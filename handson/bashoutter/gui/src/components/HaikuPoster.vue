<template>
  <v-container>
    <v-row justify="center" class="mb-4">
      <h2 class="display-1">Post your Haiku!</h2>
    </v-row>
    <v-row justify="start">
      <v-col cols="3">
        <v-text-field
          outlined
          v-model="first"
          label="五"
        ></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-text-field
          outlined
          v-model="second"
          label="七"
        ></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-text-field
          outlined
          v-model="third"
          label="五"
        ></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-text-field
          v-model="username"
          label="Your name"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="2" class="text-center">
        <v-btn
          large
          color="indigo"
          dark
          @click="postHaiku()">
          Post
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    first: "",
    second: "",
    third: "",
    username: "",
  }),
  methods: {
    postHaiku() {
      axios
        .post(this.$store.state.url + "/haiku", {
          "username": this.username,
          "first": this.first,
          "second": this.second,
          "third": this.third,
        })
        .catch(err => {
          alert(err)
        });
    }
  }
}
</script>
