<template src="./giverInfo.html"></template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import ModalDialog from "@/components/ModalDialog";

export default {
  name: "giver-info",
  components: { ModalDialog },

  data() {
    return {
      newGiver: {
        name: "",
        phone: "",
        address: "",
        city: null,
        description: "",
      },
      showAddGiver: false,
    };
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("givers", ["fetchingData", "error"]),
    ...mapGetters("cities", ["optionCities"]),
  },

  methods: {
    ...mapActions("cities", ["getCities"]),
    ...mapActions("givers", ["addGiver"]),
    handleSaveGiver() {
      this.addGiver(this.newGiver);
      this.newGiver = {};
      this.$refs.observerGiver.reset();
    },
  },
};
</script>