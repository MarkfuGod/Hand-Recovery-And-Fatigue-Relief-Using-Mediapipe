<script setup>

import MeTest from './MeTest.vue'

</script>

<template>
<button @click="back">返回主页</button>
  <div v-if="elTestShow===0">
    <div class="common-layout">
      <el-container>
        <el-header>基于手势的手部康复游戏</el-header>
        <el-main>
          <div class="image-button-wrapper">
            <div v-for="(item, index) in items" :key="index" class="image-button-container">
              <img :src="item.image" :alt="'Image ' + index" class="image">
              <button class="button" @click='show'>{{ item.buttonText }}</button>
            </div>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
<div v-else-if="elTestShow===1">
  <MeTest></MeTest>
</div>

</template>

<script>

export default {
  // components:{ElTest},
  data(){
    return{
      message:"eee22",
      elTestShow:0,
      items: [
        { image: 'src/components/images/8bf69b8ce619d69d9d31a4d9cdcb595d.jpeg', buttonText: '普通模式',shijian:'h' },
        { image: 'src/components/images/9.png', buttonText: '无尽模式',shijian:'h' },
        { image: 'src/components/images/10.png', buttonText: '闯关模式' ,shijian:'h'},
      ]
    }
  },
methods:{
    show(){
      this.elTestShow=1;
      // alert(this.elTestShow)
    },
  ss(){
    alert(this.elTestShow)
  },
  back(){
      this.elTestShow=0;
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
