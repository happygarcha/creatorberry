#!/bin/sh
cd "$(dirname "$0")" && cat main_part1.js part2_renderer.js part3_model.js part4_post.js part5_scene.js part6a_helpers.js part6b_overlay.js > main.js
