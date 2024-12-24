/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-undef */
import jQuery from "jquery";

window.$ = window.jQuery = jQuery;

("use strict");

// Spinner
// addEventListener("load", function () {
// setTimeout(function () {
//   if ($("#spinner").length > 0) {
//     $("#spinner").removeClass("show");
//   }
// }, 1);
// });
// var spinner = function () {
//   setTimeout(function () {
//     if ($("#spinner").length > 0) {
//       $("#spinner").removeClass("show");
//     }
//   }, 1);
// };
// spinner();

// Back to top button
// $(window).scroll(function () {
//   if ($(this).scrollTop() > 300) {
//     $(".back-to-top").fadeIn("slow");
//   } else {
//     $(".back-to-top").fadeOut("slow");
//   }
// });

// $(".back-to-top").click(function () {
//   $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
//   return false;
// });

// // Sidebar Toggler
// $(".sidebar-toggler").click(function () {
//   $(".sidebar, .content").toggleClass("open");
//   return false;
// });

$(window).on("scroll", () => {
  if ($(this).scrollTop() > 300) {
    $(".back-to-top").fadeIn("slow");
  } else {
    $(".back-to-top").fadeOut("slow");
  }
});

$(".back-to-top").on("click", () => {
  $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
  return false;
});

$(".sidebar-toggler").on("click", () => {
  $(".sidebar, .content").removeClass("open");
  console.log("clicked");
});
