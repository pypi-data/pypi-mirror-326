/*
 * Copyright (c) 2021, 2023 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#pragma once

#ifdef __aarch64__

namespace {

void a64_transpose_interleave_12_2x4(uint16_t *out, const uint16_t *in, size_t width, size_t in_stride, size_t height)
{
    uint16_t *pad_row = reinterpret_cast<uint16_t *>(alloca(width * sizeof(uint16_t)));

    if (height % 4) {
        memset(pad_row, 0, width * sizeof(uint16_t));
    }

    size_t out_stride = 12 * roundup<size_t>(height, 4) * sizeof(uint16_t);

    __asm__ __volatile__(
      "cmp %x[height], #0x8\n"
      "blt 10f\n"
      "1:"  // Main row loop: Head
      "mov x9, %x[in]\n"
      "add x28, x9, %x[in_stride]\n"
      "add x27, x28, %x[in_stride]\n"
      "add x26, x27, %x[in_stride]\n"
      "add x25, x26, %x[in_stride]\n"
      "mov x24, %x[width]\n"
      "add x23, x25, %x[in_stride]\n"
      "add x22, x23, %x[in_stride]\n"
      "add x20, x22, %x[in_stride]\n"
      "cmp x24, #0x18\n"
      "add %x[in], x20, %x[in_stride]\n"
      "mov x21, %x[out]\n"
      "sub %x[height], %x[height], #0x8\n"
      "blt 3f\n"
      "2:"  // Main row loop: Unroll column loop
      "ldr q21, [x9], #0x10\n"
      "ldr q20, [x28], #0x10\n"
      "sub x24, x24, #0x18\n"
      "cmp x24, #0x18\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v13.8h, v21.8h, v17.8h\n"
      "zip1 v12.8h, v20.8h, v16.8h\n"
      "ldr q19, [x25], #0x10\n"
      "ldr q18, [x23], #0x10\n"
      "zip2 v11.8h, v21.8h, v17.8h\n"
      "zip2 v10.8h, v20.8h, v16.8h\n"
      "ldr q17, [x22], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "zip1 v9.8h, v19.8h, v17.8h\n"
      "zip1 v8.8h, v18.8h, v16.8h\n"
      "ldr q21, [x9], #0x10\n"
      "ldr q20, [x28], #0x10\n"
      "zip2 v7.8h, v19.8h, v17.8h\n"
      "zip2 v6.8h, v18.8h, v16.8h\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v27.8h, v21.8h, v17.8h\n"
      "zip1 v22.8h, v20.8h, v16.8h\n"
      "ldr q19, [x25], #0x10\n"
      "ldr q18, [x23], #0x10\n"
      "zip2 v5.8h, v21.8h, v17.8h\n"
      "zip2 v4.8h, v20.8h, v16.8h\n"
      "ldr q17, [x22], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "zip1 v26.8h, v19.8h, v17.8h\n"
      "zip1 v25.8h, v18.8h, v16.8h\n"
      "ldr q21, [x9], #0x10\n"
      "ldr q20, [x28], #0x10\n"
      "zip2 v3.8h, v19.8h, v17.8h\n"
      "zip2 v2.8h, v18.8h, v16.8h\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v24.8h, v21.8h, v17.8h\n"
      "zip1 v23.8h, v20.8h, v16.8h\n"
      "ldr q19, [x25], #0x10\n"
      "ldr q18, [x23], #0x10\n"
      "zip2 v1.8h, v21.8h, v17.8h\n"
      "zip2 v0.8h, v20.8h, v16.8h\n"
      "ldr q17, [x22], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "zip1 v31.8h, v19.8h, v17.8h\n"
      "zip1 v30.8h, v18.8h, v16.8h\n"
      "zip2 v29.8h, v19.8h, v17.8h\n"
      "zip2 v28.8h, v18.8h, v16.8h\n"
      "zip1 v17.8h, v13.8h, v12.8h\n"
      "zip2 v16.8h, v13.8h, v12.8h\n"
      "str q17, [x21, #0x0]\n"
      "zip1 v18.8h, v11.8h, v10.8h\n"
      "zip2 v17.8h, v11.8h, v10.8h\n"
      "str q16, [x21, #0x10]\n"
      "zip1 v16.8h, v27.8h, v22.8h\n"
      "zip2 v22.8h, v27.8h, v22.8h\n"
      "str q18, [x21, #0x20]\n"
      "zip1 v21.8h, v9.8h, v8.8h\n"
      "zip2 v20.8h, v9.8h, v8.8h\n"
      "str q17, [x21, #0x30]\n"
      "zip1 v19.8h, v7.8h, v6.8h\n"
      "zip2 v18.8h, v7.8h, v6.8h\n"
      "str q16, [x21, #0x40]\n"
      "zip1 v17.8h, v26.8h, v25.8h\n"
      "zip2 v16.8h, v26.8h, v25.8h\n"
      "str q22, [x21, #0x50]\n"
      "str q21, [x21, #0x60]\n"
      "zip1 v27.8h, v5.8h, v4.8h\n"
      "zip2 v26.8h, v5.8h, v4.8h\n"
      "str q20, [x21, #0x70]\n"
      "zip1 v25.8h, v24.8h, v23.8h\n"
      "zip2 v24.8h, v24.8h, v23.8h\n"
      "str q19, [x21, #0x80]\n"
      "zip1 v23.8h, v1.8h, v0.8h\n"
      "zip2 v22.8h, v1.8h, v0.8h\n"
      "str q18, [x21, #0x90]\n"
      "zip1 v21.8h, v3.8h, v2.8h\n"
      "zip2 v20.8h, v3.8h, v2.8h\n"
      "str q17, [x21, #0xa0]\n"
      "zip1 v19.8h, v31.8h, v30.8h\n"
      "zip2 v18.8h, v31.8h, v30.8h\n"
      "str q16, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "zip1 v17.8h, v29.8h, v28.8h\n"
      "zip2 v16.8h, v29.8h, v28.8h\n"
      "str q27, [x21, #0x0]\n"
      "str q26, [x21, #0x10]\n"
      "str q25, [x21, #0x20]\n"
      "str q24, [x21, #0x30]\n"
      "str q23, [x21, #0x40]\n"
      "str q22, [x21, #0x50]\n"
      "str q21, [x21, #0x60]\n"
      "str q20, [x21, #0x70]\n"
      "str q19, [x21, #0x80]\n"
      "str q18, [x21, #0x90]\n"
      "str q17, [x21, #0xa0]\n"
      "str q16, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 2b\n"
      "3:"  // Main row loop: Unroll column loop skip
      "cmp x24, #0xc\n"
      "blt 5f\n"
      "4:"  // Main row loop: Column loop
      "ldr q19, [x9], #0x10\n"
      "ldr q18, [x28], #0x10\n"
      "sub x24, x24, #0xc\n"
      "cmp x24, #0xc\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v25.8h, v19.8h, v17.8h\n"
      "zip1 v24.8h, v18.8h, v16.8h\n"
      "ldr q21, [x25], #0x10\n"
      "ldr q20, [x23], #0x10\n"
      "zip2 v31.8h, v19.8h, v17.8h\n"
      "zip2 v23.8h, v18.8h, v16.8h\n"
      "ldr q17, [x22], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "zip1 v30.8h, v21.8h, v17.8h\n"
      "zip1 v29.8h, v20.8h, v16.8h\n"
      "ldr d19, [x9], #0x8\n"
      "ldr d18, [x28], #0x8\n"
      "zip2 v28.8h, v21.8h, v17.8h\n"
      "zip2 v27.8h, v20.8h, v16.8h\n"
      "ldr d17, [x27], #0x8\n"
      "ldr d16, [x26], #0x8\n"
      "zip1 v26.8h, v19.8h, v17.8h\n"
      "zip1 v22.8h, v18.8h, v16.8h\n"
      "ldr d21, [x25], #0x8\n"
      "ldr d20, [x23], #0x8\n"
      "zip1 v19.8h, v25.8h, v24.8h\n"
      "zip2 v18.8h, v25.8h, v24.8h\n"
      "ldr d17, [x22], #0x8\n"
      "ldr d16, [x20], #0x8\n"
      "zip1 v25.8h, v21.8h, v17.8h\n"
      "zip1 v24.8h, v20.8h, v16.8h\n"
      "zip1 v17.8h, v31.8h, v23.8h\n"
      "zip2 v16.8h, v31.8h, v23.8h\n"
      "str q19, [x21, #0x0]\n"
      "zip1 v23.8h, v26.8h, v22.8h\n"
      "zip2 v22.8h, v26.8h, v22.8h\n"
      "str q18, [x21, #0x10]\n"
      "zip1 v21.8h, v30.8h, v29.8h\n"
      "zip2 v20.8h, v30.8h, v29.8h\n"
      "str q17, [x21, #0x20]\n"
      "zip1 v19.8h, v28.8h, v27.8h\n"
      "zip2 v18.8h, v28.8h, v27.8h\n"
      "str q16, [x21, #0x30]\n"
      "zip1 v17.8h, v25.8h, v24.8h\n"
      "zip2 v16.8h, v25.8h, v24.8h\n"
      "str q23, [x21, #0x40]\n"
      "str q22, [x21, #0x50]\n"
      "str q21, [x21, #0x60]\n"
      "str q20, [x21, #0x70]\n"
      "str q19, [x21, #0x80]\n"
      "str q18, [x21, #0x90]\n"
      "str q17, [x21, #0xa0]\n"
      "str q16, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 4b\n"
      "5:"  // Main row loop: Column loop skip
      "cmp x24, #0x4\n"
      "blt 7f\n"
      "6:"  // Main row loop: width 4 loop: loop
      "ldr d19, [x9], #0x8\n"
      "ldr d18, [x28], #0x8\n"
      "sub x24, x24, #0x4\n"
      "cmp x24, #0x4\n"
      "ldr d17, [x27], #0x8\n"
      "ldr d16, [x26], #0x8\n"
      "zip1 v17.8h, v19.8h, v17.8h\n"
      "zip1 v16.8h, v18.8h, v16.8h\n"
      "ldr d18, [x25], #0x8\n"
      "ldr d21, [x23], #0x8\n"
      "zip1 v20.8h, v17.8h, v16.8h\n"
      "zip2 v19.8h, v17.8h, v16.8h\n"
      "ldr d17, [x22], #0x8\n"
      "ldr d16, [x20], #0x8\n"
      "zip1 v18.8h, v18.8h, v17.8h\n"
      "zip1 v16.8h, v21.8h, v16.8h\n"
      "str q20, [x21, #0x0]\n"
      "zip1 v17.8h, v18.8h, v16.8h\n"
      "zip2 v16.8h, v18.8h, v16.8h\n"
      "str q19, [x21, #0x10]\n"
      "str q17, [x21, #0x60]\n"
      "str q16, [x21, #0x70]\n"
      "add x21, x21, #0x20\n"
      "bge 6b\n"
      "7:"  // Main row loop: width 4 loop: skip
      "cmp x24, #0x1\n"
      "blt 9f\n"
      "8:"  // Main row loop: width 1 loop: loop
      "ldr h19, [x9], #0x2\n"
      "ldr h18, [x28], #0x2\n"
      "sub x24, x24, #0x1\n"
      "cmp x24, #0x1\n"
      "ldr h17, [x27], #0x2\n"
      "ldr h16, [x26], #0x2\n"
      "zip1 v17.8h, v19.8h, v17.8h\n"
      "zip1 v16.8h, v18.8h, v16.8h\n"
      "ldr h20, [x25], #0x2\n"
      "ldr h19, [x23], #0x2\n"
      "zip1 v18.8h, v17.8h, v16.8h\n"
      "ldr h17, [x22], #0x2\n"
      "ldr h16, [x20], #0x2\n"
      "zip1 v17.8h, v20.8h, v17.8h\n"
      "zip1 v16.8h, v19.8h, v16.8h\n"
      "str d18, [x21, #0x0]\n"
      "zip1 v16.8h, v17.8h, v16.8h\n"
      "str d16, [x21, #0x60]\n"
      "add x21, x21, #0x8\n"
      "bge 8b\n"
      "9:"  // Main row loop: width 1 loop: skip
      "cmp %x[height], #0x8\n"
      "add %x[out], %x[out], #0xc0\n"
      "bge 1b\n"
      "cbz %x[height], 20f\n"
      "10:"  // Main loop skip

      "11:"  // Tail row loop: Head
      "mov x9, %x[in]\n"
      "add x28, x9, %x[in_stride]\n"
      "add x27, x28, %x[in_stride]\n"
      "mov x20, %x[width]\n"
      "add x26, x27, %x[in_stride]\n"
      "cmp %x[height], #0x3\n"
      "add %x[in], x26, %x[in_stride]\n"
      "csel x26, x26, %x[pad_row], GT\n"
      "csel x27, x27, %x[pad_row], GE\n"
      "cmp %x[height], #0x1\n"
      "csel x28, x28, %x[pad_row], GT\n"
      "cmp x20, #0x18\n"
      "mov x21, %x[out]\n"
      "sub %x[height], %x[height], #0x4\n"
      "blt 13f\n"
      "12:"  // Tail row loop: Unroll column loop
      "ldr q19, [x9], #0x10\n"
      "ldr q18, [x28], #0x10\n"
      "sub x20, x20, #0x18\n"
      "cmp x20, #0x18\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v31.8h, v19.8h, v17.8h\n"
      "zip1 v30.8h, v18.8h, v16.8h\n"
      "ldr q22, [x9], #0x10\n"
      "ldr q20, [x28], #0x10\n"
      "zip2 v29.8h, v19.8h, v17.8h\n"
      "zip2 v28.8h, v18.8h, v16.8h\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v27.8h, v22.8h, v17.8h\n"
      "zip1 v21.8h, v20.8h, v16.8h\n"
      "ldr q19, [x9], #0x10\n"
      "ldr q18, [x28], #0x10\n"
      "zip2 v26.8h, v22.8h, v17.8h\n"
      "zip2 v20.8h, v20.8h, v16.8h\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v25.8h, v19.8h, v17.8h\n"
      "zip1 v24.8h, v18.8h, v16.8h\n"
      "zip2 v23.8h, v19.8h, v17.8h\n"
      "zip2 v22.8h, v18.8h, v16.8h\n"
      "zip1 v17.8h, v31.8h, v30.8h\n"
      "zip2 v16.8h, v31.8h, v30.8h\n"
      "str q17, [x21, #0x0]\n"
      "zip1 v19.8h, v29.8h, v28.8h\n"
      "zip2 v18.8h, v29.8h, v28.8h\n"
      "str q16, [x21, #0x10]\n"
      "zip1 v17.8h, v27.8h, v21.8h\n"
      "zip2 v16.8h, v27.8h, v21.8h\n"
      "str q19, [x21, #0x20]\n"
      "str q18, [x21, #0x30]\n"
      "zip1 v21.8h, v26.8h, v20.8h\n"
      "zip2 v20.8h, v26.8h, v20.8h\n"
      "str q17, [x21, #0x40]\n"
      "zip1 v19.8h, v25.8h, v24.8h\n"
      "zip2 v18.8h, v25.8h, v24.8h\n"
      "str q16, [x21, #0x50]\n"
      "add x21, x21, %x[out_stride]\n"
      "zip1 v17.8h, v23.8h, v22.8h\n"
      "zip2 v16.8h, v23.8h, v22.8h\n"
      "str q21, [x21, #0x0]\n"
      "str q20, [x21, #0x10]\n"
      "str q19, [x21, #0x20]\n"
      "str q18, [x21, #0x30]\n"
      "str q17, [x21, #0x40]\n"
      "str q16, [x21, #0x50]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 12b\n"
      "13:"  // Tail row loop: Unroll column loop skip
      "cmp x20, #0xc\n"
      "blt 15f\n"
      "14:"  // Tail row loop: Column loop
      "ldr q21, [x9], #0x10\n"
      "ldr q18, [x28], #0x10\n"
      "sub x20, x20, #0xc\n"
      "cmp x20, #0xc\n"
      "ldr q17, [x27], #0x10\n"
      "ldr q16, [x26], #0x10\n"
      "zip1 v24.8h, v21.8h, v17.8h\n"
      "zip1 v23.8h, v18.8h, v16.8h\n"
      "ldr d20, [x9], #0x8\n"
      "ldr d19, [x28], #0x8\n"
      "zip2 v22.8h, v21.8h, v17.8h\n"
      "zip2 v18.8h, v18.8h, v16.8h\n"
      "ldr d17, [x27], #0x8\n"
      "ldr d16, [x26], #0x8\n"
      "zip1 v21.8h, v20.8h, v17.8h\n"
      "zip1 v20.8h, v19.8h, v16.8h\n"
      "zip1 v17.8h, v24.8h, v23.8h\n"
      "zip2 v16.8h, v24.8h, v23.8h\n"
      "str q17, [x21, #0x0]\n"
      "zip1 v19.8h, v22.8h, v18.8h\n"
      "zip2 v18.8h, v22.8h, v18.8h\n"
      "str q16, [x21, #0x10]\n"
      "zip1 v17.8h, v21.8h, v20.8h\n"
      "zip2 v16.8h, v21.8h, v20.8h\n"
      "str q19, [x21, #0x20]\n"
      "str q18, [x21, #0x30]\n"
      "str q17, [x21, #0x40]\n"
      "str q16, [x21, #0x50]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 14b\n"
      "15:"  // Tail row loop: Column loop skip
      "cmp x20, #0x4\n"
      "blt 17f\n"
      "16:"  // Tail row loop: width 4 loop: loop
      "ldr d18, [x9], #0x8\n"
      "ldr d19, [x28], #0x8\n"
      "sub x20, x20, #0x4\n"
      "cmp x20, #0x4\n"
      "ldr d17, [x27], #0x8\n"
      "ldr d16, [x26], #0x8\n"
      "zip1 v18.8h, v18.8h, v17.8h\n"
      "zip1 v16.8h, v19.8h, v16.8h\n"
      "zip1 v17.8h, v18.8h, v16.8h\n"
      "zip2 v16.8h, v18.8h, v16.8h\n"
      "str q17, [x21, #0x0]\n"
      "str q16, [x21, #0x10]\n"
      "add x21, x21, #0x20\n"
      "bge 16b\n"
      "17:"  // Tail row loop: width 4 loop: skip
      "cmp x20, #0x1\n"
      "blt 19f\n"
      "18:"  // Tail row loop: width 1 loop: loop
      "ldr h19, [x9], #0x2\n"
      "ldr h18, [x28], #0x2\n"
      "sub x20, x20, #0x1\n"
      "cmp x20, #0x1\n"
      "ldr h17, [x27], #0x2\n"
      "ldr h16, [x26], #0x2\n"
      "zip1 v17.8h, v19.8h, v17.8h\n"
      "zip1 v16.8h, v18.8h, v16.8h\n"
      "zip1 v16.8h, v17.8h, v16.8h\n"
      "str d16, [x21, #0x0]\n"
      "add x21, x21, #0x8\n"
      "bge 18b\n"
      "19:"  // Tail row loop: width 1 loop: skip
      "cmp %x[height], #0x1\n"
      "add %x[out], %x[out], #0x60\n"
      "bge 11b\n"
      "20:"  // Done

      : [height] "+&r" (height), [in] "+&r" (in), [out] "+&r" (out)
      : [in_stride] "r" (in_stride), [out_stride] "r" (out_stride), [pad_row] "r" (pad_row), [width] "r" (width)
      : "cc", "memory", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "x9", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28"
    );
}

} // anonymous namespace

template<>
void Transform<12, 4, true, VLType::None>(
    bfloat16 *out, const bfloat16 *in, int stride, int x0, int xmax, int k0, int kmax)
{
    a64_transpose_interleave_12_2x4(
        reinterpret_cast<uint16_t *>(out),
        reinterpret_cast<const uint16_t *>(in + k0 * stride + x0),
        (xmax-x0) * sizeof(bfloat16) / 2,
        stride * sizeof(bfloat16),
        (kmax-k0)
    );
}

#endif
