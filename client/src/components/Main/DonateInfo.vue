<template src="./donateInfo.html"></template>

<script>
import { mapState, mapActions } from "vuex";
import ModalDialog from "@/components/ModalDialog";

export default {
  name: "donate-info",
  components: { ModalDialog },

  data() {
    return {
      donate: {
        donate: "",
        description: "",
      },
      showAddDonate: false,
    };
  },

  props: {
    takerId: { default: "" },
    editObject: { default: "" },
    isNew: { default: false },
    isNewInline: { default: false },
    isEdit: { default: false },
  },

  computed: {
    ...mapState("users", ["user"]),
    ...mapState("takers", ["fetchingData", "error"]),
  },

  methods: {
    ...mapActions("takers", ["addDonate", "updateDonate"]),
    handleSaveDonate() {
      if (this.isEdit) {
        this.updateDonate(this.donate);
      } else {
        this.addDonate(this.donate);
        this.donate = { taker: this.takerId };
      }
      this.$refs.observerDonate.reset();
    },
  },

  created() {
    this.donate.taker = this.takerId;
    if (this.isEdit) {
      this.donate = { ...this.editObject };
    }
  },
};
</script>