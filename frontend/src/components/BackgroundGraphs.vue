<template>
  <canvas id="background"></canvas>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  var canvas = document.getElementById("background"),
    can_w = parseInt(canvas.getAttribute("width")),
    can_h = parseInt(canvas.getAttribute("height")),
    ctx = canvas.getContext("2d");

  var BALL_NUM = 40;

  // var ball = {
  // 	x: 0,
  // 	y: 0,
  // 	vx: 0,
  // 	vy: 0,
  // 	r: 0,
  // 	alpha: 1,
  // 	phase: 0,
  // }

  var ball_color = {
      r: 204,
      g: 204,
      b: 0,
    },
    R = 2,
    balls = [],
    alpha_f = 0.03,
    // alpha_phase = 0,
    // Line
    link_line_width = 0.8,
    dis_limit = 260,
    // add_mouse_point = true,
    mouse_ball = {
      x: 0,
      y: 0,
      vx: 0,
      vy: 0,
      r: 0,
      type: "mouse",
    };

  function getRandomSpeed(pos) {
    var min = -1,
      max = 1;
    switch (pos) {
      case "top":
        return [randomNumFrom(min, max), randomNumFrom(0.1, max)];

      case "right":
        return [randomNumFrom(min, -0.1), randomNumFrom(min, max)];

      case "bottom":
        return [randomNumFrom(min, max), randomNumFrom(min, -0.1)];

      case "left":
        return [randomNumFrom(0.1, max), randomNumFrom(min, max)];

      default:
        return;
    }
  }
  function randomArrayItem(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }
  function randomNumFrom(min, max) {
    return Math.random() * (max - min) + min;
  }

  function getRandomBall() {
    var pos = randomArrayItem(["top", "right", "bottom", "left"]);
    switch (pos) {
      case "top":
        return {
          x: randomSidePos(can_w),
          y: -R,
          vx: getRandomSpeed("top")[0],
          vy: getRandomSpeed("top")[1],
          r: R,
          alpha: 1,
          phase: randomNumFrom(0, 10),
        };

      case "right":
        return {
          x: can_w + R,
          y: randomSidePos(can_h),
          vx: getRandomSpeed("right")[0],
          vy: getRandomSpeed("right")[1],
          r: R,
          alpha: 1,
          phase: randomNumFrom(0, 10),
        };

      case "bottom":
        return {
          x: randomSidePos(can_w),
          y: can_h + R,
          vx: getRandomSpeed("bottom")[0],
          vy: getRandomSpeed("bottom")[1],
          r: R,
          alpha: 1,
          phase: randomNumFrom(0, 10),
        };

      case "left":
        return {
          x: -R,
          y: randomSidePos(can_h),
          vx: getRandomSpeed("left")[0],
          vy: getRandomSpeed("left")[1],
          r: R,
          alpha: 1,
          phase: randomNumFrom(0, 10),
        };
    }
  }
  function randomSidePos(length) {
    return Math.ceil(Math.random() * length);
  }

  function renderBalls() {
    Array.prototype.forEach.call(balls, function (b) {
      if (!Object.prototype.hasOwnProperty.call(b, "type")) {
        ctx.fillStyle =
          "rgba(" +
          ball_color.r +
          "," +
          ball_color.g +
          "," +
          ball_color.b +
          "," +
          b.alpha +
          ")";
        ctx.beginPath();
        ctx.arc(b.x, b.y, R, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.fill();
      }
    });
  }

  function updateBalls() {
    var new_balls = [];
    Array.prototype.forEach.call(balls, function (b) {
      b.x += b.vx;
      b.y += b.vy;

      if (b.x > -50 && b.x < can_w + 50 && b.y > -50 && b.y < can_h + 50) {
        new_balls.push(b);
      }

      // alpha change
      b.phase += alpha_f;
      b.alpha = Math.abs(Math.cos(b.phase));
    });

    balls = new_balls.slice(0);
  }

  function renderLines() {
    var fraction, alpha;
    for (var i = 0; i < balls.length; i++) {
      for (var j = i + 1; j < balls.length; j++) {
        fraction = getDisOf(balls[i], balls[j]) / dis_limit;

        if (fraction < 1) {
          alpha = (1 - fraction).toString();

          ctx.strokeStyle = "rgba(150,150,150," + alpha + ")";
          ctx.lineWidth = link_line_width;

          ctx.beginPath();
          ctx.moveTo(balls[i].x, balls[i].y);
          ctx.lineTo(balls[j].x, balls[j].y);
          ctx.stroke();
          ctx.closePath();
        }
      }
    }
  }

  function getDisOf(b1, b2) {
    var delta_x = Math.abs(b1.x - b2.x),
      delta_y = Math.abs(b1.y - b2.y);

    return Math.sqrt(delta_x * delta_x + delta_y * delta_y);
  }

  function addBallIfy() {
    if (balls.length < BALL_NUM) {
      balls.push(getRandomBall());
    }
  }

  function render() {
    ctx.clearRect(0, 0, can_w, can_h);

    renderBalls();

    renderLines();

    updateBalls();

    addBallIfy();

    window.requestAnimationFrame(render);
  }

  function initBalls(num) {
    for (var i = 1; i <= num; i++) {
      balls.push({
        x: randomSidePos(can_w),
        y: randomSidePos(can_h),
        vx: getRandomSpeed("top")[0],
        vy: getRandomSpeed("top")[1],
        r: R,
        alpha: 1,
        phase: randomNumFrom(0, 10),
      });
    }
  }

  function initCanvas() {
    canvas.setAttribute("width", window.innerWidth);
    canvas.setAttribute("height", window.innerHeight);

    can_w = parseInt(canvas.getAttribute("width"));
    can_h = parseInt(canvas.getAttribute("height"));
  }
  window.addEventListener("resize", function () {
    initCanvas();
  });

  function goMovie() {
    initCanvas();
    initBalls(BALL_NUM);
    window.requestAnimationFrame(render);
  }
  goMovie();

  canvas.addEventListener("mouseenter", function () {
    balls.push(mouse_ball);
  });
  canvas.addEventListener("mouseleave", function () {
    var new_balls = [];
    Array.prototype.forEach.call(balls, function (b) {
      if (!Object.prototype.hasOwnProperty.call(b, "type")) {
        new_balls.push(b);
      }
    });
    balls = new_balls.slice(0);
  });
  canvas.addEventListener("mousemove", function (e) {
    var err = e || window.event;
    mouse_ball.x = err.pageX;
    mouse_ball.y = err.pageY;
  });
});
</script>

<style>
canvas {
  position: fixed;
  top: 0;
  left: 0;
  background-color: var(--dark);
  z-index: -100;
}
</style>
