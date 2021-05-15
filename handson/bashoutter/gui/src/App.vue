<template>
  <v-app>
    <v-app-bar
      app
      color="blue"
      dark
    >
      <v-btn icon>
        <v-icon>mdi-alpha-b-box</v-icon>
      </v-btn>
      <v-toolbar-title>Bashoutter</v-toolbar-title>      
    </v-app-bar>

    <v-content>
      <EndpointUrl/>
      <HaikuPoster/>
      <HaikuList/>
    </v-content>
  </v-app>
</template>

<script>
import EndpointUrl from "./components/EndpointUrl"
import HaikuList from "./components/HaikuList"
import HaikuPoster from "./components/HaikuPoster"

export default {
  name: "App",
  components: {
    EndpointUrl,
    HaikuList,
    HaikuPoster,
  },
  data: () => ({
    //
  }),
};
</script>
