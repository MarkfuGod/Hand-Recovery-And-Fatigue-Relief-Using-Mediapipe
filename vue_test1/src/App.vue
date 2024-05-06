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
<div class="app-background">
  <div class="videoContainer">
      <video class="fullscreenVideo" id="bgVid" playsinline="" autoplay="" muted="" loop="" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;z-index: -1;">
        <source src="src\components\images\bg.mp4" type="video/mp4">
      </video>
    </div>
<button @click="back" class="back-button"><div class=custom-font>返回主页</div></button>
 <img src="./components/images/logo.png" alt="Logo" class="centered-image" style="display: block;
  margin: 0 auto; /* 水平居中 */
  max-width: 20%; /* 确保图片不会超出屏幕宽度 */
  height: auto; opacity:10">
  <div v-if="elTestShow===0">
    <div class="common-layout">
      <el-container>
        <el-header class="title" style="color: aqua;"><div class=custom-font>基于手势的手部康复游戏</div></el-header>
        <el-main>
          <div v-if="elShow===0">
            <el-input v-model="input" placeholder="请输入用户名" style="width: 50%;margin-left: 44%;display: block;justify-content: center;font-family: douyu;"></el-input>
            <el-input v-model="input1" placeholder="请输入密码" style="width: 50%;margin-left: 44%;display: block;justify-content: center;"></el-input>
           <el-button type="primary" @click="ok" style="width: 5%; margin-left: 44%"><div class=custom-font>登录</div></el-button>
<el-button type="success" @click="registerNo" style="width: 5%; "><div class=custom-font>注册</div></el-button>

          </div>
          <div v-if="elShow===2">
            <el-input v-model="input2" placeholder="请输入用户名" style="width: 50%;margin-left: 44%;display: block;justify-content: center;"></el-input>
            <el-input v-model="input3" placeholder="请输入密码" style="width: 50%;margin-left: 44%;display: block;justify-content: center;"></el-input>
            <el-button type="success" @click="registerOk" style="width: 10%; margin-left: 44%">注册</el-button>
          </div>
          <div v-if="elShow===1" class="image-button-wrapper">
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
      elShow: 0,
      input: '',
      input1:'',
      input2:'',
      input3:'',
      items: [
        { image: 'images/8bf69b8ce619d69d9d31a4d9cdcb595d.jpeg', buttonText: '普通模式',shijian:'h' },
        { image: 'images/9.png', buttonText: '无尽模式',shijian:'h' },
        { image: 'images/10.png', buttonText: '闯关模式' ,shijian:'h'},
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
  },
  ok(){
      this.elShow=1;
      alert(this.elShow)
  },
  registerNo(){
      this.elShow=2;
  },
  registerOk(){
      this.elShow=0;
      alert("注册成功")
  }
}
}
</script>


<style scoped>

@import './assets/styles.css';
.app-background {
  background-image: url('./components/images/'); /* 设置背景图像 */
  background-size: cover; /* 背景图像覆盖整个容器 */
  background-position: center; /* 背景图像居中显示 */
  height: 100vh; /* 设置容器高度为视口高度 */
  opacity: 1;
  z-index: 1;
}
.custom-font {
  font-family: douyu; /* 替换为您的字体系列 */
}

</style>
