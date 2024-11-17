<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useMessage, NInput, NForm, NFormItem, NButton,darkTheme, NConfigProvider, NInputNumber} from 'naive-ui' //
import type { FormInst } from 'naive-ui'
import axios from 'axios';

export default defineComponent({

  components:
  {
    NForm,
    NFormItem,
    NButton,
    NInput,
    NInputNumber
  },
  setup()
  {
    const formRef = ref<FormInst | null>(null)
    return{
      formRef,
      formValue: ref({
        flowRate: 0,
        valuePercentOpen:0,
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
  data()
  {
    return
    {
          // const formRef = ref<FormInst | null>(null)
          // const message = useMessage();
    }
  },

methods:{
   handleSubmit() {
      // Perform form submission logic here
      console.log("Form submitted... FlowRate:", this.formValue.flowRate);
      console.log("ValveOpenPercent: ", this.formValue.valuePercentOpen);
      axios
      .post('API-URL',JSON.stringify(this.formValue, null, 2))
      .then((res)=>
      {
          console.log(res);

      })
      .catch(()=>{})
    }
}
})
</script>
<template>

     <n-form
      ref="formRef"
      inline
      :label-width="80"
      :model="formValue"
    >
      <!-- :rules="rules" -->

      <!-- @submit.prevent="handleSubmit" -->

      <n-form-item label="Flow Rate" path="flowRate">
        <n-input-number v-model:value="formValue.flowRate" clearable />
      </n-form-item>
      <n-form-item label="Valve Percent Open" path="flowRate">
          <n-input-number
          v-model:value="formValue.valuePercentOpen"
          :show-button="false"
          :min="0"
          :max="100">
          <template #suffix>
            %
          </template>
        </n-input-number>
      </n-form-item>
      <n-form-item>
        <n-button @click="handleSubmit">
          Submit
        </n-button>
        </n-form-item>
    </n-form>
    <!-- <pre>{{ JSON.stringify(formValue, null, 2) }}</pre> -->
     <p>{{  }}</p>

</template>

<style scoped>

</style>
