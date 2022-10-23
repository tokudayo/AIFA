// Copyright 2020 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.google.mediapipe.apps.posetrackinggpu;

import android.os.Bundle;
import android.util.Log;
import android.graphics.Bitmap;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmark;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmarkList;
import com.google.mediapipe.framework.PacketGetter;
import com.google.protobuf.InvalidProtocolBufferException;
import com.google.mediapipe.framework.AndroidPacketGetter;
import io.socket.client.IO;
import io.socket.client.Socket;
import java.net.URISyntaxException;
import java.io.ByteArrayOutputStream;

/** Main activity of MediaPipe pose tracking app. */
public class MainActivity extends com.google.mediapipe.apps.basic.MainActivity {
  private static final String TAG = "MainActivity";

  private static final String OUTPUT_LANDMARKS_STREAM_NAME = "pose_landmarks";
  private Socket mSocket;
  {
    try {
      mSocket = IO.socket("http://192.168.1.214:13051");
      Log.e(TAG, "Success to init socket.");
    } catch (URISyntaxException e) {
      Log.e(TAG, "Failed to init socket.", e);
    }
  }

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    mSocket.connect();

    // To show verbose logging, run:
    // adb shell setprop log.tag.MainActivity VERBOSE
    if (Log.isLoggable(TAG, Log.VERBOSE)) {
      processor.addPacketCallback(
          "throttled_input_video_cpu",
          (packet) -> {
            Log.v(TAG, "Received image with ts: ");
            Bitmap image = AndroidPacketGetter.getBitmapFromRgba(packet);
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            image.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArray = stream.toByteArray();
            mSocket.emit("image_mobile", byteArray, System.currentTimeMillis());
            image.recycle();
          });
      processor.addPacketCallback(
          OUTPUT_LANDMARKS_STREAM_NAME,
          (packet) -> {
            Log.v(TAG, "Received pose landmarks packet.");
            try {
              byte[] landmarksRaw = PacketGetter.getProtoBytes(packet);
              NormalizedLandmarkList poseLandmarks = NormalizedLandmarkList.parseFrom(landmarksRaw);
              Log.v(
                  TAG,
                  "[TS:"
                      + packet.getTimestamp()
                      + "] "
                      + getPoseLandmarksDebugString(poseLandmarks));
              mSocket.emit("landmark_mobile", getPoseLandmarksDebugString(poseLandmarks), System.currentTimeMillis());
            } catch (InvalidProtocolBufferException exception) {
              Log.e(TAG, "Failed to get proto.", exception);
            }
          });
    }
  }

  private static String getPoseLandmarksDebugString(NormalizedLandmarkList poseLandmarks) {
    String poseLandmarkStr = "[";
    int landmarkIndex = 0;
    for (NormalizedLandmark landmark : poseLandmarks.getLandmarkList()) {
      poseLandmarkStr += "["
          + landmark.getX()
          + ", "
          + landmark.getY()
          + ", "
          + landmark.getZ()
          + ", "
          + landmark.getVisibility()
          + "],";
      ++landmarkIndex;
    }
    poseLandmarkStr = poseLandmarkStr.substring(0, poseLandmarkStr.length() - 1);
    poseLandmarkStr += "]";
    return poseLandmarkStr;
  }
}
