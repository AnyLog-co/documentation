---
title: Video Streaming
description: Ingest video streams from IP cameras, RTSP feeds, YouTube, and local files — with optional AI inference — into AnyLog.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

AnyLog can connect to video streams, record segmented clips to a blob database, and optionally run AI inference (e.g. YOLOv5 object detection) via a gRPC server.

---

## Supported protocols

| Protocol | Latency | Typical use |
|---|---|---|
| RTMP | ~1–2s | Live ingest (OBS, Twitch, YouTube) |
| RTMPS | ~1–2s | Secure RTMP over TLS |
| SRT | ~1–2s | Professional contribution feeds over unreliable networks |
| RTSP | ~1–5s | IP cameras and surveillance |
| HTTP/HTTPS / HLS | ~1–5s | Standard HTTP streams, m3u8 playlists |
| Local file (MP4, MOV, MKV…) | 0s | Stored video files on disk |

---

## Prerequisites

- MongoDB connected as the blob database (stores video segments)
- PostgreSQL or SQLite connected as the SQL database (stores metadata and detections)
- (Optional) A YOLOv5 inference gRPC server for object detection — see <a href="{{ '/docs/Managing-Data-Southbound/grpc/' | relative_url }}">gRPC</a>

---

## Step 1 — Connect databases

```anylog
# Blob database (MongoDB)
<connect dbms customers where type = mongo and ip = 127.0.0.1 and port = 27017 and user = demo and password = passwd>

# SQL database
<connect dbms customers where type = psql and ip = 127.0.0.1 and port = 5432 and user = demo and password = passwd>
```

---

## Step 2 — Set video variables

```anylog
video_url   = "https://www.youtube.com/watch?v=rnXIjl_Rzy4"   # Times Square live
video_host  = 127.0.0.1
video_port  = 8888
video_table = video_table
```

Sample stream URLs:
- Abbey Road London: `https://www.youtube.com/watch?v=57w2gYXjRic`
- Times Square: `https://www.youtube.com/watch?v=rnXIjl_Rzy4`

---

## Step 3 — Import the display function

```anylog
import function where import_name = imshow and lib = external_lib.video_processing.cv2_stream_imshow and method = init_class
set function params where import_name = imshow and param_name = port and param_type = int and param_value = !video_port
set function params where import_name = imshow and param_name = host and param_value = !video_host
```

---

## Step 4 — Connect to the video stream

### Without inference

```anylog
<video connect where
  name           = youtube and
  protocol       = https and
  interface      = url and
  address        = !video_url and
  video_dbms     = customers and
  video_table    = video_table>
```

### With object detection inference

First start the gRPC inference client (see <a href="{{ '/docs/Managing-Data-Southbound/grpc/' | relative_url }}">gRPC</a> for setup):

```anylog
<run grpc client where
  name = yolov5 and ip = 127.0.0.1 and port = 50051 and
  grpc_dir = /app/AnyLog-Network/external_lib/frame_modeling and
  proto = infer and function = PredictStream and
  request = PredictRequest and response = PredictResponse and
  service = InferenceService and debug = false and invoke = true>
```

Then connect with detection columns:

```anylog
<video connect where
  name                 = youtube and
  protocol             = https and
  interface            = url and
  address              = !video_url and
  video_dbms           = customers and
  video_table          = video_table and
  detection_dbms       = customers and
  detection_table      = detection_table and
  detection_column     = person and
  detection_column     = car and
  detection_column     = truck and
  detection_column     = bus and
  recording_segment_time = 1 and
  detection_ignore_time  = 10>
```

### `video connect` parameter reference

| Parameter | Description |
|---|---|
| `name` | Logical name for this stream connection |
| `protocol` | Stream protocol: `https`, `rtsp`, `rtmp`, `srt`, etc. |
| `interface` | `url` for network streams |
| `address` | Stream URL or file path |
| `video_dbms` | Blob database for storing video segments |
| `video_table` | Table name for video metadata |
| `detection_dbms` | Database for inference results |
| `detection_table` | Table for inference results |
| `detection_column` | Object class to detect (repeat for each class) |
| `recording_segment_time` | Length of each recorded clip in minutes |
| `detection_ignore_time` | Seconds to suppress duplicate detections of the same object |

---

## Step 5 — Start the stream

```anylog
# Without inference
run video stream where name = youtube and import_display = imshow

# With inference
run video stream where name = youtube and import_display = imshow and grpc_name = yolov5
```

View the live stream in a browser:
```
http://[video_host]:[video_port]/stream/[name]
```

---

## Step 6 — Stop the stream

```anylog
exit video where name = youtube
```

---

## Querying video data

### Video segments (no inference)

```anylog
run client () sql customers format=json and stat=false \
  "select file, timestamp from video_table order by timestamp DESC limit 20"
```

### Detection results (with inference)

```anylog
run client () sql customers format=json and stat=false \
  "select file, timestamp, car, truck, bus, person from detection_table order by timestamp DESC limit 20"
```

---

## Architecture notes

The stream runs three internal threads:

| Thread | Role |
|---|---|
| Capture | Reads frames from the video source |
| Display | Shows frames in the real-time browser window |
| Storage | Writes frames to disk in H.264/yuv420p segments |

- Display buffer: max 2 frames (prevents lag)
- Recording buffer: max 120 frames (~4 seconds at 30fps)
- Detections are batched (25 entries per write) and deduplicated using `detection_ignore_time`