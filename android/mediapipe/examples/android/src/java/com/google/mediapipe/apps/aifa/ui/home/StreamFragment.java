// Copyright 2019 The MediaPipe Authors.
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

package com.google.mediapipe.apps.aifa.ui.home;

import com.google.mediapipe.apps.aifa.R;

import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.graphics.SurfaceTexture;
import android.view.LayoutInflater;
import android.os.Bundle;
import android.util.Log;
import android.util.Size;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import com.google.mediapipe.components.CameraHelper;
import com.google.mediapipe.components.CameraXPreviewHelper;
import com.google.mediapipe.components.ExternalTextureConverter;
import com.google.mediapipe.components.FrameProcessor;
import com.google.mediapipe.components.PermissionHelper;
import com.google.mediapipe.framework.AndroidAssetUtil;
import com.google.mediapipe.glutil.EglManager;
import com.google.android.material.snackbar.Snackbar;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmark;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmarkList;
import com.google.mediapipe.framework.PacketGetter;
import com.google.protobuf.InvalidProtocolBufferException;
import java.net.URISyntaxException;

import androidx.fragment.app.Fragment;

public class StreamFragment extends Fragment {
    private static final String TAG = "MainActivity";

    // Flips the camera-preview frames vertically by default, before sending them
    // into FrameProcessor
    // to be processed in a MediaPipe graph, and flips the processed frames back
    // when they are
    // displayed. This maybe needed because OpenGL represents images assuming the
    // image origin is at
    // the bottom-left corner, whereas MediaPipe in general assumes the image origin
    // is at the
    // top-left corner.
    // NOTE: use "flipFramesVertically" in manifest metadata to override this
    // behavior.
    private static final boolean FLIP_FRAMES_VERTICALLY = true;

    // Number of output frames allocated in ExternalTextureConverter.
    // NOTE: use "converterNumBuffers" in manifest metadata to override number of
    // buffers. For
    // example, when there is a FlowLimiterCalculator in the graph, number of
    // buffers should be at
    // least `max_in_flight + max_in_queue + 1` (where max_in_flight and
    // max_in_queue are used in
    // FlowLimiterCalculator options). That's because we need buffers for all the
    // frames that are in
    // flight/queue plus one for the next frame from the camera.
    private static final int NUM_BUFFERS = 2;

    static {
        // Load all native libraries needed by the app.
        System.loadLibrary("mediapipe_jni");
        try {
            System.loadLibrary("opencv_java3");
        } catch (java.lang.UnsatisfiedLinkError e) {
            // Some example apps (e.g. template matching) require OpenCV 4.
            System.loadLibrary("opencv_java4");
        }
    }

    // Sends camera-preview frames into a MediaPipe graph for processing, and
    // displays the processed
    // frames onto a {@link Surface}.
    protected FrameProcessor processor;
    // Handles camera access via the {@link CameraX} Jetpack support library.
    protected CameraXPreviewHelper cameraHelper;

    // {@link SurfaceTexture} where the camera-preview frames can be accessed.
    private SurfaceTexture previewFrameTexture;
    // {@link SurfaceView} that displays the camera-preview frames processed by a
    // MediaPipe graph.
    private SurfaceView previewDisplayView;

    // Creates and manages an {@link EGLContext}.
    private EglManager eglManager;
    // Converts the GL_TEXTURE_EXTERNAL_OES texture from Android camera into a
    // regular texture to be
    // consumed by {@link FrameProcessor} and the underlying MediaPipe graph.
    private ExternalTextureConverter converter;

    // ApplicationInfo for retrieving metadata defined in the manifest.
    private ApplicationInfo applicationInfo;

    private Snackbar snackbar;

    private int cameraWidth = 0;
    private int cameraHeight = 0;

    // Websocket
    private static final String OUTPUT_LANDMARKS_STREAM_NAME = "pose_landmarks";
    private Socket mSocket;
    {
        try {
            mSocket = IO.socket("wss://aifa.one");
        } catch (URISyntaxException e) {
        }
    }

    public static StreamFragment newInstance(String exercise) {
        StreamFragment streamFragment = new StreamFragment();
    
        Bundle args = new Bundle();
        args.putString("exercise", exercise);
        streamFragment.setArguments(args);
    
        return streamFragment;
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
            ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);
        View root = inflater.inflate(R.layout.fragment_stream, container, false);

        return root;
    }

    public void onViewCreated(View view,
            Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        super.onActivityCreated(savedInstanceState);
        // DisplayMetrics displayMetrics = new DisplayMetrics();
        // getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        // int height = displayMetrics.heightPixels;
        // int width = displayMetrics.widthPixels;

        try {
            applicationInfo = getActivity().getPackageManager().getApplicationInfo(getActivity().getPackageName(), PackageManager.GET_META_DATA);
        } catch (NameNotFoundException e) {
            Log.e(TAG, "Cannot find application info: " + e);
        }

        mSocket.connect();

        mSocket.on("alert", onNewMessage);
        mSocket.emit("join", java.util.UUID.randomUUID().toString());

        previewDisplayView = new SurfaceView(getActivity());
        setupPreviewDisplayView(view);

        // Initialize asset manager so that MediaPipe native libraries can access the
        // app assets, e.g.,
        // binary graphs.
        AndroidAssetUtil.initializeNativeAssetManager(getActivity());
        eglManager = new EglManager(null);
        long nativeContext = eglManager.getNativeContext();

        processor = new FrameProcessor(
                getActivity(),
                nativeContext,
                applicationInfo.metaData.getString("binaryGraphName"),
                applicationInfo.metaData.getString("inputVideoStreamName"),
                applicationInfo.metaData.getString("outputVideoStreamName"));
        processor
                .getVideoSurfaceOutput()
                .setFlipY(
                        applicationInfo.metaData.getBoolean("flipFramesVertically", FLIP_FRAMES_VERTICALLY));

        PermissionHelper.checkAndRequestCameraPermissions(getActivity());

        processor.addPacketCallback(
                OUTPUT_LANDMARKS_STREAM_NAME,
                (packet) -> {
                    try {
                        byte[] landmarksRaw = PacketGetter.getProtoBytes(packet);
                        NormalizedLandmarkList poseLandmarks = NormalizedLandmarkList.parseFrom(landmarksRaw);
                        mSocket.emit("landmark_mobile", getPoseLandmarksString(poseLandmarks),
                                System.currentTimeMillis(), getArguments().getString("exercise"), cameraWidth, cameraHeight);
                    } catch (InvalidProtocolBufferException exception) {
                    }
                });
    }

    private Emitter.Listener onNewMessage = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            getActivity().runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    String data = (String) args[0];
                    try {
                        snackbar.setText(data);
                    } catch (Exception e) {
                        snackbar = Snackbar.make(getActivity().findViewById(android.R.id.content), data, Snackbar.LENGTH_INDEFINITE);
                        snackbar.show();
                    }
                }
            });
        }
    };

    @Override
    public void onResume() {
        super.onResume();
        converter = new ExternalTextureConverter(
                eglManager.getContext(),
                applicationInfo.metaData.getInt("converterNumBuffers", NUM_BUFFERS));
        converter.setFlipY(
                applicationInfo.metaData.getBoolean("flipFramesVertically", FLIP_FRAMES_VERTICALLY));
        converter.setConsumer(processor);
        if (PermissionHelper.cameraPermissionsGranted(getActivity())) {
            startCamera();
        }
    }

    @Override
    public void onPause() {
        super.onPause();
        converter.close();

        // Hide preview display until we re-open the camera again.
        previewDisplayView.setVisibility(View.GONE);
    }

    @Override
    public void onRequestPermissionsResult(
            int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        PermissionHelper.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    protected void onCameraStarted(SurfaceTexture surfaceTexture) {
        previewFrameTexture = surfaceTexture;
        // Make the display view visible to start showing the preview. This triggers the
        // SurfaceHolder.Callback added to (the holder of) previewDisplayView.
        previewDisplayView.setVisibility(View.VISIBLE);
    }

    protected Size cameraTargetResolution() {
        return null; // No preference and let the camera (helper) decide.
    }

    public void startCamera() {
        cameraHelper = new CameraXPreviewHelper();
        previewFrameTexture = converter.getSurfaceTexture();
        cameraHelper.setOnCameraStartedListener(
                surfaceTexture -> {
                    onCameraStarted(surfaceTexture);
                });
        CameraHelper.CameraFacing cameraFacing = applicationInfo.metaData.getBoolean("cameraFacingFront", false)
                ? CameraHelper.CameraFacing.FRONT
                : CameraHelper.CameraFacing.BACK;
        cameraHelper.startCamera(
                getActivity(), cameraFacing, previewFrameTexture, cameraTargetResolution());
    }

    protected Size computeViewSize(int width, int height) {
        return new Size(width, height);
    }

    protected void onPreviewDisplaySurfaceChanged(
            SurfaceHolder holder, int format, int width, int height) {
        // (Re-)Compute the ideal size of the camera-preview display (the area that the
        // camera-preview frames get rendered onto, potentially with scaling and
        // rotation)
        // based on the size of the SurfaceView that contains the display.
        Size viewSize = computeViewSize(width, height);
        Size displaySize = cameraHelper.computeDisplaySizeFromViewSize(viewSize);
        boolean isCameraRotated = cameraHelper.isCameraRotated();

        cameraWidth = isCameraRotated ? displaySize.getHeight() : displaySize.getWidth();
        cameraHeight = isCameraRotated ? displaySize.getWidth() : displaySize.getHeight();

        // Configure the output width and height as the computed display size.
        converter.setDestinationSize(
                isCameraRotated ? displaySize.getHeight() : displaySize.getWidth(),
                isCameraRotated ? displaySize.getWidth() : displaySize.getHeight());
    }

    private void setupPreviewDisplayView(View view) {
        previewDisplayView.setVisibility(View.GONE);
        ViewGroup viewGroup = view.findViewById(R.id.preview_display_layout);
        viewGroup.addView(previewDisplayView);

        previewDisplayView
                .getHolder()
                .addCallback(
                        new SurfaceHolder.Callback() {
                            @Override
                            public void surfaceCreated(SurfaceHolder holder) {
                                processor.getVideoSurfaceOutput().setSurface(holder.getSurface());
                            }

                            @Override
                            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
                                onPreviewDisplaySurfaceChanged(holder, format, width, height);
                            }

                            @Override
                            public void surfaceDestroyed(SurfaceHolder holder) {
                                processor.getVideoSurfaceOutput().setSurface(null);
                            }
                        });
    }

    private static String getPoseLandmarksString(NormalizedLandmarkList poseLandmarks) {
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

    @Override
    public void onDestroy() {
        super.onDestroy();

        snackbar.dismiss();
        mSocket.disconnect();
        mSocket.off("alert", onNewMessage);
    }
}
