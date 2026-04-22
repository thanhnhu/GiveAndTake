<template src="./takerInfo.html"></template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import ModalDialog from "@/components/ModalDialog";

export default {
  name: "taker-info",
  components: { ModalDialog },

  data() {
    return {
      newTaker: {
        name: "",
        phone: "",
        address: "",
        city: null,
        description: "",
      },
      showAddTaker: false,
    };
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("takers", ["fetchingData", "error"]),
    ...mapGetters("cities", ["optionCities"]),
  },

  methods: {
    ...mapActions("takers", ["addTaker"]),
    handleSaveTaker() {
      this.addTaker(this.newTaker);
      this.newTaker = {};
      this.$refs.observerTaker.reset();
    },
  },
};
</script>