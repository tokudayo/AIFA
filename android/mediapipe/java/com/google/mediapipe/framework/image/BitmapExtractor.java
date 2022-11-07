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

/**
 * Utility for extracting {@link android.graphics.Bitmap} from {@link Image}.
 *
 * <p>Currently it only supports {@link Image} with {@link Image#STORAGE_TYPE_BITMAP}, otherwise
 * {@link IllegalArgumentException} will be thrown.
 */
public final class BitmapExtractor {

  /**
   * Extracts a {@link android.graphics.Bitmap} from an {@link Image}.
   *
   * @param image the image to extract {@link android.graphics.Bitmap} from.
   * @return the {@link android.graphics.Bitmap} stored in {@link Image}
   * @throws IllegalArgumentException when the extraction requires unsupported format or data type
   *     conversions.
   */
  public static Bitmap extract(Image image) {
    ImageContainer imageContainer = image.getContainer(Image.STORAGE_TYPE_BITMAP);
    if (imageContainer != null) {
      return ((BitmapImageContainer) imageContainer).getBitmap();
    } else {
      // TODO: Support ByteBuffer -> Bitmap conversion.
      throw new IllegalArgumentException(
          "Extracting Bitmap from an Image created by objects other than Bitmap is not"
              + " supported");
    }
  }

  private BitmapExtractor() {}
}
