<template>
  <div>
  </div>

  <section id="demos" class="invisible">


    <div class="image-container">
      <img :class="borderClass(0)" src="src/components/images/com_4.jpeg" alt="Image 1">
      <img :class="borderClass(1)" src="src/components/images/com_5.jpg" alt="Image 2">
      <img :class="borderClass(2)" src="src/components/images/com_23.png" alt="Image 3">
      <img :class="borderClass(3)" src="src/components/images/com_24.png" alt="Image 4">
      <img :class="borderClass(4)" src="src/components/images/com_38.jpg" alt="Image 5">
    </div>

    <div id="liveView" class="videoView">
      <button id="webcamButton" class="mdc-button mdc-button--raised">
        <span class="mdc-button__ripple"></span>



        <span class="mdc-button__label">开始测试</span>
      </button>
      <div style="position: relative;">
        <video id="webcam" ref="video" autoplay playsinline></video>
        <canvas class="output_canvas" id="output_canvas" width="1280" height="720" style="position: absolute; left: 0px; top: 0px;"></canvas>
        <p id='gesture_output' class="output"></p>
      </div>
    </div>
  </section>
</template>



<script>
import {
  GestureRecognizer,
  FilesetResolver,
  DrawingUtils
} from "@mediapipe/tasks-vision";

export default {
  data() {
    return {
      bianse:1,


      worker: null,
      camera: null,
      gestureRecognizer: null,
      runningMode: "IMAGE",
      enableWebcamButton: null,
      webcamRunning: false,
      videoHeight: "360px",
      videoWidth: "480px",
      demosSection: null,
      lastVideoTime: -1,
      results: undefined,
    };
  },


  computed: {
    borderClass() {
      return (index) => {
        return this.bianse === index ? 'border-show' : 'border-hide';
      }
    }
  },


  async mounted() {
    this.demosSection = document.getElementById("demos");
    this.createGestureRecognizer();
    this.enableWebcamButton = document.getElementById("webcamButton");
    if (this.hasGetUserMedia()) {
      this.enableWebcamButton.addEventListener("click", this.enableCam);
    } else {
      console.warn("getUserMedia() is not supported by your browser");
    }

    this.$nextTick(() => {
      this.demosSection = document.getElementById("demos");
      this.createGestureRecognizer();
      this.enableWebcamButton = document.getElementById("webcamButton");
      if (this.hasGetUserMedia()) {
        this.enableWebcamButton.addEventListener("click", this.enableCam);
      } else {
        console.warn("getUserMedia() is not supported by your browser");
      }
    });
  },
  methods: {
    async createGestureRecognizer() {
      const vision = await FilesetResolver.forVisionTasks(
          // "@mediapipe/tasks-vision/wasm"
          "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
      );
      this.gestureRecognizer = await GestureRecognizer.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
          // "",
              "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
          delegate: "GPU"
        },
        runningMode: this.runningMode
      });
      this.demosSection.classList.remove("invisible");
    },
    async handleClick(event) {
      if (!this.gestureRecognizer) {
        alert("Please wait for gestureRecognizer to load");
        return;
      }

      if (this.runningMode === "VIDEO") {
        this.runningMode = "IMAGE";
        await this.gestureRecognizer.setOptions({ runningMode: "IMAGE" });
      }
      // Remove all previous landmarks
      const allCanvas = event.target.parentNode.getElementsByClassName("canvas");
      for (var i = allCanvas.length - 1; i >= 0; i--) {
        const n = allCanvas[i];
        n.parentNode.removeChild(n);
      }

      const results = this.gestureRecognizer.recognize(event.target);

      // View results in the console to see their format
      console.log(results);
      if (results.gestures.length > 0) {
        const p = event.target.parentNode.childNodes[3];
        p.setAttribute("class", "info");

        const categoryName = results.gestures[0][0].categoryName;
        const categoryScore = parseFloat(
            results.gestures[0][0].score * 100
        ).toFixed(2);
        const handedness = results.handednesses[0][0].displayName;

        p.innerText = `GestureRecognizer: ${categoryName}\n Confidence: ${categoryScore}%\n Handedness: ${handedness}`;
        p.style =
            "left: 0px;" +
            "top: " +
            event.target.height +
            "px; " +
            "width: " +
            (event.target.width - 10) +
            "px;";

        const canvas = document.createElement("canvas");
        canvas.setAttribute("class", "canvas");
        canvas.setAttribute("width", event.target.naturalWidth + "px");
        canvas.setAttribute("height", event.target.naturalHeight + "px");
        canvas.style =
            "left: 0px;" +
            "top: 0px;" +
            "width: " +
            event.target.width +
            "px;" +
            "height: " +
            event.target.height +
            "px;";

        event.target.parentNode.appendChild(canvas);
        const canvasCtx = canvas.getContext("2d");
        const drawingUtils = new DrawingUtils(canvasCtx);
        for (const landmarks of results.landmarks) {
          drawingUtils.drawConnectors(
              landmarks,
              GestureRecognizer.HAND_CONNECTIONS,
              {
                color: "#00FF00",
                lineWidth: 5
              }
          );
          drawingUtils.drawLandmarks(landmarks, {
            color: "#FF0000",
            lineWidth: 1
          });
        }
      }
    },
    hasGetUserMedia() {
      return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    },
    async enableCam(event) {
      if (!this.gestureRecognizer) {
        alert("Please wait for gestureRecognizer to load");
        return;
      }

      if (this.webcamRunning === true) {
        this.webcamRunning = false;
        this.enableWebcamButton.innerText = "ENABLE PREDICTIONS";
      } else {
        this.webcamRunning = true;
        this.enableWebcamButton.innerText = "DISABLE PREDICTIONS";
      }

      // getUsermedia parameters.
      const constraints = {
        video: true
      };

      // Activate the webcam stream.
      navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        this.$refs.video.srcObject = stream;
        this.$refs.video.play();
        this.$refs.video.addEventListener("loadeddata", this.predictWebcam);
      });
    },
    async predictWebcam() {
      const webcamElement = this.$refs.video;
      const canvasElement = this.$refs.canvas;
      const canvasCtx = canvasElement.getContext("2d");

      // Now let's start detecting the stream.
      if (this.runningMode === "IMAGE") {
        this.runningMode = "VIDEO";
        await this.gestureRecognizer.setOptions({ runningMode: "VIDEO" });
      }
      let nowInMs = Date.now();
      if (webcamElement.currentTime !== this.lastVideoTime) {
        this.lastVideoTime = webcamElement.currentTime;
        this.results = this.gestureRecognizer.recognizeForVideo(webcamElement, nowInMs);
      }

      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      const drawingUtils = new DrawingUtils(canvasCtx);

      canvasElement.style.height = this.videoHeight;
      webcamElement.style.height = this.videoHeight;
      canvasElement.style.width = this.videoWidth;
      webcamElement.style.width = this.videoWidth;

      if (this.results.landmarks) {
        for (const landmarks of this.results.landmarks) {
          drawingUtils.drawConnectors(
              landmarks,
              GestureRecognizer.HAND_CONNECTIONS,
              {
                color: "#00FF00",
                lineWidth: 5
              }
          );
          drawingUtils.drawLandmarks(landmarks, {
            color: "#FF0000",
            lineWidth: 2
          });
        }
      }
      canvasCtx.restore();

      // Call this function again to keep predicting when the browser is ready.
      if (this.webcamRunning === true) {
        window.requestAnimationFrame(this.predictWebcam);
      }
    }
  },
};
</script>
<style>
@use "@material";
body {
  font-family: roboto;
  margin: 2em;
  color: #3d3d3d;
  --mdc-theme-primary: #007f8b;
  --mdc-theme-on-primary: #f1f3f4;
}

h1 {
  color: #007f8b;
}

h2 {
  clear: both;
}

video {
  clear: both;
  display: block;
  transform: rotateY(180deg);
  -webkit-transform: rotateY(180deg);
  -moz-transform: rotateY(180deg);
  height: 280px;
}

section {
  opacity: 1;
  transition: opacity 500ms ease-in-out;
}

.removed {
  display: none;
}

.invisible {
  opacity: 0.2;
}

.detectOnClick {
  position: relative;
  float: left;
  width: 48%;
  margin: 2% 1%;
  cursor: pointer;
}
.videoView {
  position: absolute;
  float: left;
  width: 48%;
  margin: 2% 1%;
  cursor: pointer;
  min-height: 500px;
}

.videoView p,
.detectOnClick p {
  padding-top: 5px;
  padding-bottom: 5px;
  background-color: #007f8b;
  color: #fff;
  border: 1px dashed rgba(255, 255, 255, 0.7);
  z-index: 2;
  margin: 0;
}

.highlighter {
  background: rgba(0, 255, 0, 0.25);
  border: 1px dashed #fff;
  z-index: 1;
  position: absolute;
}

.canvas {
  z-index: 1;
  position: absolute;
  pointer-events: none;
}

.output_canvas {
  transform: rotateY(180deg);
  -webkit-transform: rotateY(180deg);
  -moz-transform: rotateY(180deg);
}

.detectOnClick {
  z-index: 0;
  font-size: calc(8px + 1.2vw);
}
.image-container {
  display: flex;
  justify-content: space-between;
}

.image-container img {
  width: 100px;
  height: 100px;
  object-fit: cover; /* 这将保持图片的纵横比 */
  //border: 2px solid red;
}

.border-show {
  border: 2px solid red;
}
.border-hide {
  border: none;
}

.detectOnClick img {
  width: 45vw;
}
.output {
  display: none;
  width: 100%;
  font-size: calc(8px + 1.2vw);
}
</style>