<script setup>

import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import ElText from './ElTest.vue'
import image1 from './assets/6.jpg'
import image3 from './components/images/10.png'
import MeTest from './MeTest.vue'
import image2 from './components/images/8bf69b8ce619d69d9d31a4d9cdcb595d.jpeg'

</script>

<template>
<div>
<button @click="back" class="back-button">返回主页</button>
  <div v-if="elTestShow===0">
    <div class="common-layout">
      <el-container>
        <el-header class="title">基于手势的手部康复游戏</el-header>
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
<!--  <button @click="show">33</button>-->
<!--  <button @click="ss">44</button>-->
<!--&lt;!&ndash;  <ElText></ElText>&ndash;&gt;-->
<!--  <div class="common-layout" >-->
<!--    <ElText v-if="elTestShow===1"></ElText>-->
<!--  </div>-->
<!--<div v-show="elTestShow===0">-->
<!--  <MeTest ></MeTest>-->
<!--</div>-->
<!--  <MeTest></MeTest>-->
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
      alert(this.elTestShow)
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

@import './assets/styles.css';

</style>
