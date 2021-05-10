<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="6">
        <v-text-field
          v-model="endpoint_url"
          label="API Endpoint URL"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
  }),
  computed: {
    endpoint_url: {
      get () {
        return this.$store.state.url
      },
      set (value) {
        this.$store.commit("set_url", value)
      }
    }
  }

}
</script>
