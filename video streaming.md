# AnyLog Video Streaming Configuration Guide

## Overview
This guide covers the initialization and configuration options for video streaming in AnyLog, including database connections, detection models, and display settings.

## Protocol Support

The system supports the following video protocols:

| Protocol | Typical Latency | Use Case | Supported |
|----------|----------------|----------|-----------|
| **RTMP** (Real-Time Messaging Protocol) | ~1–2 sec | Older Adobe Flash-era protocol. Widely used for ingesting streams (YouTube Live, Twitch, OBS → server) | ✅ |
| **SRT** (Secure Reliable Transport) | ~1–2 sec | Secure, low-latency, robust over unreliable networks. Great for professional contribution feeds | ✅ |
| **RTSP** (Real-Time Streaming Protocol) | ~1–5 sec | Used in IP cameras and surveillance systems. Can be converted for web playback | ✅ |
| **HTTP/HTTPS** (progressive/HLS) | ~1–5 sec | Standard HTTP streaming, HLS (m3u8 playlists) or progressive streams | ✅ |
| **RTMPS** | ~1–2 sec | Secure RTMP (RTMP over TLS). Used for cloud services like YouTube Live ingest | ✅ |
| **Local video file** (MP4, MOV, MKV, etc.) | 0 sec | Stored video files on disk. Read directly by PyAV/FFmpeg | ✅ |

## Basic Initialization Structure

### 1. Bob Database Connection
```
connect dbms <database_name> 
  where type = mongo 
  and ip = <ip_address> 
  and port = <port_number> 
  and user = <username> 
  and password = <password>
```

**Parameters:**
- `database_name`: Name of the database (e.g., "customers")
- `type`: Database type (e.g., "mongo")
- `ip`: Database IP address (e.g., "127.0.0.1")
- `port`: Database port number (e.g., 27017)
- `user`: Database username
- `password`: Database password

### 2. SQL Database Connection
```
connect dbms <database_name> 
  where type = psql 
  and ip = <ip_address> 
  and port = <port_number> 
  and user = <username> 
  and password = <password>
```

**Parameters:**
- `database_name`: Name of the database (e.g., "customers")
- `type`: Database type (e.g., "psql")
- `ip`: Database IP address (e.g., "127.0.0.1")
- `port`: Database port number (e.g., 27017)
- `user`: Database username
- `password`: Database password

### 3. Video Configuration Variables
```
video_url = "<video_source_url>"   # URL from which to consume video stream
video_host = <host_ip>             # IP to display consumed video
video_port = <port_number>         # Port to display consumed video
video_table = <video_table>        # video database table name 
```

**Parameters:**
- `video_url`: Source URL (e.g., YouTube URL, RTSP stream, local file path)
- `video_host`: Host IP for video display (e.g., "127.0.0.1" or "0.0.0.0")
- `video_port`: Port for video display (e.g., 8888)
- `video_table`: SQL DB table name
e.g.,
```
video_url = "https://www.youtube.com/watch?v=rnXIjl_Rzy4"
video_host = 127.0.0.1
video_port = 8888
video_table=video_table
```

### 4. Import built-in video streaming libraries
```
import function where import_name = imshow and lib = external_lib.video_processing.cv2_stream_imshow and method = init_class
set function params where import_name = imshow and param_name = port and param_type = int and param_value = !video_port
set function params where import_name = imshow and param_name = host and param_value = !video_host
```

### 5. [Optional] Enable Detection
To enable detection, deploy YOLO model in docker container. 
See this [README](https://github.com/AnyLog-co/AnyLog-Video-Inference-Models/blob/main/README.md) for instructions.
Note that AnyLog offloads inference to a gRPC server. This server can run on the same physical machine or on a different machine. 

#### Connect to gRPC server
This creates an AnyLog-managed gRPC client that can call your YOLOv5 inference service. You’re pointing AnyLog at the directory that contains the generated protobuf/stub files (or the .proto + generated outputs, depending on your setup), then telling it which service, RPC function, and request/response message types to use.

| Parameter  | Example value                                                        | What it does                                                                                    |
| ---------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `name`     | `yolov5`                                                             | Logical name for this gRPC client in AnyLog                                                     |
| `ip`       | `127.0.0.1`                                                          | gRPC server host/IP (localhost in your case)                                                    |
| `port`     | `50051`                                                              | gRPC server port                                                                                |
| `grpc_dir` | `/Users/roy/Github-Repos/AnyLog-Network/external_lib/frame_modeling` | Path AnyLog uses to locate protobuf definitions / generated stubs (your `infer_pb2*` artifacts) |
| `proto`    | `infer`                                                              | Proto “module” / base filename (e.g., `infer.proto` → `infer_pb2.py`)                           |
| `service`  | `InferenceService`                                                   | gRPC service name inside the proto                                                              |
| `function` | `PredictStream`                                                      | RPC method to invoke (here: stream-stream)                                                      |
| `request`  | `PredictRequest`                                                     | Request message type name                                                                       |
| `response` | `PredictResponse`                                                    | Response message type name                                                                      |
| `debug`    | `false`                                                              | Enables/disables extra logging (request/response details)                                       |
| `invoke`   | `true`                                                               | If `true`, AnyLog will attempt to initialize and invoke/connect immediately                     |

AnyLog command
```
<run grpc client where name=yolov5 and ip = 127.0.0.1 and port = 50051 and grpc_dir = /Users/roy/Github-Repos/AnyLog-Network/external_lib/frame_modeling 
and proto = infer and function = PredictStream and request = "PredictRequest" and response = "PredictResponse" 
and service = InferenceService and debug = false and invoke = true>
```

### 6. Video connect

In AnyLog operator connect to a  video stream, set the following values in the CLI:
| Field                  | Value             | Comment                                                                  |
| ---------------------- | ----------------- | ------------------------------------------------------------------------ |
| name                   | `youtube`         |                                                                          |
| protocol               | `https`           |                                                                          |
| interface              | `url`             |                                                                          |
| address                | `!video_url`      |                                                                          |
| video_dbms             | `customers`       |                                                                          |
| video_table            | `video_table`     |                                                                          |
| detection_dbms         | `customers`       | DBMS where detections are written to                                     |
| detection_table        | `detection_table` | Table to store inference results managed in `detection_dbms`             |
| detection_column       | `person`          | Detection column; column names are the inference predictions             |
| detection_column       | `car`             | Inference model outputs `"car"`                                          |
| detection_column       | `truck`           | Inference model outputs `"truck"`                                        |
| detection_column       | `bus`             | Inference model outputs `"bus"`                                          |
| recording_segment_time | `1`               | Record 1-minute clips                                                    |
| detection_ignore_time  | `10`              | Time to ignore multiple detections if they have the same value (seconds) |

Example command:
```
<video connect where
    name = youtube and
    protocol = https and
    interface = url and
    address = !video_url and
    video_dbms = customers and
    video_table = video_table and
    detection_dbms = customers and
    detection_table = detection_table and
    detection_column = person and
    detection_column = car and
    detection_column = truck and
    detection_column = bus and
    recording_segment_time = 1 and
    detection_ignore_time = 10
>
```
#### Detection Columns
Multiple detection columns can be specified to track different object types:
```
and detection_column = person
and detection_column = car
and detection_column = truck
and detection_column = bus
```

#### Setup no inference on video stream
```
<video connect where
    name = youtube and
    protocol = https and
    interface = url and
    address = !video_url and
    video_dbms = customers and
    video_table = video_table and
>
```


### 7. Running the Video Stream

#### Start Stream Command
No detection
```
run video stream where name = youtube and import_display = imshow
```
With detection
```
run video stream where name = youtube and import_display = imshow and grpc_name = yolov5
```

View video at 

`http://!video_host:!video_port/stream/[video_connect_name]`

### 8. Exit video stream
Kill display server and stop processing video stream data
```
exit video where name = [logical name]
```

## Complete Example

```
# 1. Connect to blobs database
connect dbms customers 
  where type = mongo 
  and ip = 127.0.0.1 
  and port = 27017 
  and user = demo 
  and password = passwd

# 2. Connect to SQL database
connect dbms customers 
  where type = psql 
  and ip = 127.0.0.1 
  and port = 5432 
  and user = demo 
  and password = passwd

# 2. Set video variables
video_url = "https://www.youtube.com/watch?v=rnXIjl_Rzy4"
video_host = 127.0.0.1
video_port = 8888
video_table=video_table

# 3. Import display function

import function where import_name = imshow and lib = external_lib.video_processing.cv2_stream_imshow and method = init_class

set function params where import_name = imshow and param_name = port and param_type = int and param_value = !video_port

set function params where import_name = imshow and param_name = host and param_value = !video_host

# 4a. Create video connection (no inference)
<video connect where
    name = youtube and
    protocol = https and
    interface = url and
    address = !video_url and
    video_dbms = customers and
    video_table = video_table and
>

# 4b. Connect gRPC client and Create video connection with inference
<run grpc client where name=yolov5 and ip = 127.0.0.1 and port = 50051 and grpc_dir = /Users/roy/Github-Repos/AnyLog-Network/external_lib/frame_modeling 
and proto = infer and function = PredictStream and request = "PredictRequest" and response = "PredictResponse" 
and service = InferenceService and debug = false and invoke = true>

<video connect where
    name = youtube and
    protocol = https and
    interface = url and
    address = !video_url and
    video_dbms = customers and
    video_table = video_table and
    detection_dbms = customers and
    detection_table = detection_table and
    detection_column = person and
    detection_column = car and
    detection_column = truck and
    detection_column = bus and
    recording_segment_time = 1 and
    detection_ignore_time = 10
>

# 5a. Run the stream (no inference)

run video stream where name = youtube and import_display = imshow

# 5b. Run the stream (with inference)
run video stream where name = youtube and import_display = imshow and grpc_name = yolov5

# 6. View stream in browser
http://!video_host:!video_port/stream/youtube

# 6. Stop video stream
exit video where name = youtube

```

## Key Features

### Frame Processing
- **Frame Queue**: Maximum 2 frames for display (prevents buffering lag)
- **Recording Queue**: Maximum 120 frames (~4 seconds at 30fps)
- **Frame Lock**: Thread-safe frame access between capture, display, and recording

### Detection Processing
- Detections are batched (25 entries before writing to database)
- Duplicate detections are filtered based on `detection_ignore_time`
- Bounding boxes are drawn on frames
- Insights are generated by comparing consecutive detections

### Recording
- **Segmented Recording**: Video split into segments based on `recording_segment_time`
- **Codec**: H.264 (libx264)
- **Pixel Format**: yuv420p
- **Variable Frame Rate**: Supports dynamic frame rates

### Thread Architecture
1. **Capture Thread**: Reads frames from video source
2. **Display Thread**: Shows frames in real-time window
3. **Storage Thread**: Writes frames to disk in segments

## Error Handling
The system includes comprehensive error handling for:
- Connection failures
- File write failures

## Statistics Tracking
The system tracks:
- Total frames processed
- Detections made
- Detections considered (after filtering)
- JSON files written (detection batches)
