
<script lang="ts">
import { defineComponent } from 'vue'
import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5'
import { NP,NText, NUploadDragger,NUpload, NIcon } from 'naive-ui'

export default defineComponent({
  components: {
    ArchiveIcon,
    NP,
    NText,
    NUploadDragger,
    NUpload,
    NIcon
  },
  methods:
  {
    // handleUpload()
    // {
    //     console.log("MEOWMEOW")
    // }
  }
})
</script>

<template>
  <!-- multiple

     -->
  <n-upload
    directory-dnd
    action="https://2l5gzv3a4jz2p6zao6bmpnezva0kbije.lambda-url.us-east-1.on.aws/"
    :max="1"
  >
    <n-upload-dragger>
      <div style="margin-bottom: 12px">
        <n-icon class="image" size="48" :depth="3">
          <ArchiveIcon />
        </n-icon>
      </div>
      <n-text style="font-size: 16px">
        Click or drag a file to this area to upload
      </n-text>
      <n-p depth="3" style="margin: 8px 0 0 0">
        Strictly prohibit from uploading sensitive information. For example,
        your bank card PIN or your credit card expiry date.
      </n-p>
    </n-upload-dragger>
  </n-upload>
</template>

<style scoped>

</style>
