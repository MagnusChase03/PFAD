<script lang="ts">
import { defineComponent, ref } from 'vue'
import {
  useMessage,
  NInput,
  NForm,
  NFormItem,
  NButton,
  darkTheme,
  NConfigProvider,
  NInputNumber,
} from 'naive-ui' //
import type { FormInst } from 'naive-ui'
import axios from 'axios'

export default defineComponent({
  components: {
    NForm,
    NFormItem,
    NButton,
    NInput,
    NInputNumber,
  },
  setup() {
    const formRef = ref<FormInst | null>(null)
    return {
      formRef,
      formValue: ref({
        filename: '',
      }),
      // rules: {
      //   flowRate:
      //   {
      //     required:true,
      //     message: "Please input the flow rate.",
      //     trigger: 'input',
      //   },
      //   valvePercentOpen:{
      //     required:true,
      //     message: "Please input the flow rate.",
      //     trigger: ['input', 'blur'],
      //   }
      // },
    }
  },
  data() {
    return
    {
      // const formRef = ref<FormInst | null>(null)
      // const message = useMessage();
    }
  },

  methods: {
    handleSubmit() {
      // Perform form submission logic here
      // console.log("Form submitted... FlowRate:", this.formValue.flowRate);
      // console.log("ValveOpenPercent: ", this.formValue.valuePercentOpen);
      //JSON.stringify({"fileName":this.formValue.filename}, null, 2)
     fetch('https://b63boc6lac5bmsmmddazum22um0mvswp.lambda-url.us-east-1.on.aws/', {
      method: 'POST',
        mode: 'cors', // Enables CORS

      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*', // This will not affect actual CORS behavior
      },
      body: JSON.stringify({
        filename: this.formValue.filename,
      }),
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error('There was a problem with the fetch operation:', error);
  });

    },
  },
})
</script>
<template>
  <n-form ref="formRef" inline :label-width="80" :model="formValue">
    <!-- :rules="rules" -->

    <!-- @submit.prevent="handleSubmit" -->

    <n-form-item label="File name" path="flowRate">
      <n-input v-model:value="formValue.filename" clearable />
    </n-form-item>
    <n-form-item>
      <n-button @click="handleSubmit"> Submit </n-button>
    </n-form-item>
  </n-form>
  <!-- <pre>{{ JSON.stringify(formValue, null, 2) }}</pre> -->
</template>

<style scoped></style>
