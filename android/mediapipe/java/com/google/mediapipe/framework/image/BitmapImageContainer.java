/* Copyright 2022 The MediaPipe Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

package com.google.mediapipe.framework.image;

import android.graphics.Bitmap;
import com.google.mediapipe.framework.image.Image.ImageFormat;

class BitmapImageContainer implements ImageContainer {

  private final Bitmap bitmap;
  private final ImageProperties properties;

  public BitmapImageContainer(Bitmap bitmap) {
    this.bitmap = bitmap;
    this.properties =
        ImageProperties.builder()
            .setImageFormat(convertFormatCode(bitmap.getConfig()))
            .setStorageType(Image.STORAGE_TYPE_BITMAP)
            .build();
  }

  public Bitmap getBitmap() {
    return bitmap;
  }

  @Override
  public ImageProperties getImageProperties() {
    return properties;
  }

  @Override
  public void close() {
    bitmap.recycle();
  }

  @ImageFormat
  static int convertFormatCode(Bitmap.Config config) {
    switch (config) {
      case ALPHA_8:
        return Image.IMAGE_FORMAT_ALPHA;
      case ARGB_8888:
        return Image.IMAGE_FORMAT_RGBA;
      default:
        return Image.IMAGE_FORMAT_UNKNOWN;
    }
  }
}
