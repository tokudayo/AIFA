# Copyright 2019 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

licenses(["notice"])

android_library(
    name = "aifa_lib",
    srcs = glob(["*.java"]),
    manifest = "AndroidManifest.xml",
    resource_files = glob(["res/**"]),
    visibility = ["//visibility:public"],
    deps = [
        "//mediapipe/java/com/google/mediapipe/components:android_camerax_helper",
        "//mediapipe/java/com/google/mediapipe/components:android_components",
        "//mediapipe/java/com/google/mediapipe/framework:android_framework",
        "//mediapipe/java/com/google/mediapipe/glutil",
        "//third_party:androidx_appcompat",
        "//third_party:androidx_constraint_layout",
        "//third_party:opencv",
        "@maven//:androidx_concurrent_concurrent_futures",
        "@maven//:com_google_guava_guava",
        "@maven//:com_squareup_retrofit2_retrofit",
        "@maven//:com_squareup_retrofit2_converter_gson",
        "@maven//:com_google_code_gson_gson",
        "@maven//:com_google_android_material_material",
        "@maven//:androidx_navigation_navigation_runtime",
        "@maven//:androidx_drawerlayout_drawerlayout",
        "@maven//:androidx_navigation_navigation_ui",
        "@maven//:androidx_navigation_navigation_fragment",
        "@maven//:androidx_annotation_annotation",
        "@maven//:androidx_fragment_fragment",
        "@maven//:androidx_lifecycle_lifecycle_viewmodel",
        "@maven//:androidx_lifecycle_lifecycle_livedata_core",
    ],
)

# Manifest common across example apps.
exports_files(
    srcs = ["AndroidManifest.xml"],
)

# Native dependencies to perform edge detection in the Hello World example.
cc_binary(
    name = "libmediapipe_jni.so",
    linkshared = 1,
    linkstatic = 1,
    deps = [
        "//mediapipe/java/com/google/mediapipe/framework/jni:mediapipe_framework_jni",
        "//mediapipe/graphs/pose_tracking:pose_tracking_gpu_deps",
    ],
)

# Converts the .so cc_binary into a cc_library, to be consumed in an android_binary.
cc_library(
    name = "mediapipe_jni_lib",
    srcs = [":libmediapipe_jni.so"],
    alwayslink = 1,
)

# Hello World example app.
android_binary(
    name = "aifa",
    srcs = glob(["**/*.java"]),
    assets = [
        "//mediapipe/graphs/pose_tracking:pose_tracking_gpu.binarypb",
        "//mediapipe/modules/pose_landmark:pose_landmark_full.tflite",
        "//mediapipe/modules/pose_detection:pose_detection.tflite",
    ],
    assets_dir = "",
    manifest = "AndroidManifest.xml",
    manifest_values = {
        "applicationId": "com.google.mediapipe.apps.aifa",
        "appName": "AIFA",
        "mainActivity": ".MainActivity",
        "cameraFacingFront": "True",
        "binaryGraphName": "pose_tracking_gpu.binarypb",
        "inputVideoStreamName": "input_video",
        "outputVideoStreamName": "output_video",
        "flipFramesVertically": "True",
        "converterNumBuffers": "2",
    },
    multidex = "native",
    deps = [
        ":aifa_lib",
        ":mediapipe_jni_lib",
        "//mediapipe/framework/formats:landmark_java_proto_lite",
        "//mediapipe/java/com/google/mediapipe/framework:android_framework",
        "@com_google_protobuf//:protobuf_javalite",
        "@maven//:io_socket_socket_io_client",
        "//mediapipe/java/com/google/mediapipe/components:android_camerax_helper",
        "//mediapipe/java/com/google/mediapipe/components:android_components",
        "//mediapipe/java/com/google/mediapipe/glutil",
        "//third_party:androidx_appcompat",
        "//third_party:androidx_constraint_layout",
        "//third_party:opencv",
        "@maven//:androidx_concurrent_concurrent_futures",
        "@maven//:com_google_guava_guava",
        "@maven//:com_squareup_retrofit2_retrofit",
        "@maven//:com_squareup_retrofit2_converter_gson",
        "@maven//:com_google_code_gson_gson",
        "@maven//:com_google_android_material_material",
        "@maven//:androidx_navigation_navigation_runtime",
        "@maven//:androidx_drawerlayout_drawerlayout",
        "@maven//:androidx_navigation_navigation_ui",
        "@maven//:androidx_navigation_navigation_fragment",
        "@maven//:androidx_annotation_annotation",
        "@maven//:androidx_fragment_fragment",
        "@maven//:androidx_lifecycle_lifecycle_viewmodel",
        "@maven//:androidx_lifecycle_lifecycle_livedata_core",
    ],
)
