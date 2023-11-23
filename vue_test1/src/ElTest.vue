<template>
  <div>
    <div class="common-layout">
      <el-container>
        <el-header>Header</el-header>
        <el-main>
          <div class="image-button-wrapper">
            <div v-for="(item, index) in items" :key="index" class="image-button-container">
              <img :src="item.image" :alt="'Image ' + index" class="image">
              <button class="button" @click='h'>{{ item.buttonText }}</button>
            </div>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import MeTest from "@/MeTest.vue";

export default {
  data() {
    return {
      items: [
        { image: 'src/components/images/8bf69b8ce619d69d9d31a4d9cdcb595d.jpeg', buttonText: '普通模式',shijian:'h' },
        { image: 'src/components/images/9.png', buttonText: '无尽模式',shijian:'h' },
        { image: 'src/components/images/10.png', buttonText: '闯关模式' ,shijian:'h'},
      ]
    }
  },
  methods:{
    h(){
      MeTest.data().elTestShow=0;
      alert(MeTest.data().elTestShow)
    }
  }
}
</script>

<style scoped>
.common-layout {
  display: flex;
  justify-content: space-around;
}

.image-button-wrapper {
  display: flex;
  justify-content: space-around;
}

.image-button-container {
  width: fit-content;
}

.image {
  width: 200px;
  height: 200px;
  object-fit: cover;
}

.button {
  width: 100%;
}
</style>