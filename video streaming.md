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

### 1. Database Connection
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

### 2. Video Configuration Variables
```
video_url = "<video_source_url>"
video_host = <host_ip>
video_port = <port_number>
```

**Parameters:**
- `video_url`: Source URL (e.g., YouTube URL, RTSP stream, local file path)
- `video_host`: Host IP for video display (e.g., "127.0.0.1")
- `video_port`: Port for video display (e.g., 8888)

### 3. Enable Detection
```
set enable_detections = true
set default_dbms = <database_name>
```

## Function Imports

### Display Function (cv2_stream_imshow)
```
import function 
  where import_name = imshow 
  and lib = external_lib.video_processing.cv2_stream_imshow 
  and method = init_class

set function params 
  where import_name = imshow 
  and param_name = port 
  and param_type = int 
  and param_value = !video_port

set function params 
  where import_name = imshow 
  and param_name = host 
  and param_value = !video_host
```

**Parameters:**
- `import_name`: Reference name for the function
- `lib`: Library path for the display module
- `method`: Initialization method
- `port`: Display port (integer)
- `host`: Display host IP

### Detection Function (YOLO)
```
import function 
  where import_name = initiate_yolo 
  and lib = external_lib.frame_modeling.yolo_detection 
  and method = init_class
```

#### YOLO Configuration Parameters

**Module Type:**
```
set function params 
  where import_name = initiate_yolo 
  and param_name = module_type 
  and param_value = darknet
```

**Classes (Detection Categories):**
```
set function params 
  where import_name = initiate_yolo 
  and param_name = classes 
  and param_type = list 
  and param_value = []
```
- Empty list `[]` means detect all available classes
- Can specify specific classes to detect

**Model Weights:**
```
set function params 
  where import_name = initiate_yolo 
  and param_name = module_path1 
  and param_value = <path_to_weights_file>
```
- Example: `/path/to/yolov4-tiny.weights`

**Model Configuration:**
```
set function params 
  where import_name = initiate_yolo 
  and param_name = module_path2 
  and param_value = <path_to_config_file>
```
- Example: `/path/to/yolov4-tiny.cfg`

**COCO Names:**
```
set function params 
  where import_name = initiate_yolo 
  and param_name = coco_path 
  and param_value = <path_to_coco_names>
```
- Example: `/path/to/coco.names`

## Video Connection Configuration

### Connection Command
```xml
<video connect 
  where name = <connection_name>
  and protocol = <protocol_type>
  and interface = <interface_type>
  and address = <video_source>
  and video_dbms = <video_database>
  and video_table = <video_table_name>
  and detection_dbms = <detection_database>
  and detection_table = <detection_table_name>
  and detection_column = <object_type_1>
  and detection_column = <object_type_2>
  and detection_column = <object_type_3>
  and recording_segment_time = <minutes>
  and detection_ignore_time = <seconds>
>
```

### Connection Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `name` | Unique identifier for the connection | "youtube" |
| `protocol` | Connection protocol | "https", "rtsp", "rtmp" |
| `interface` | Interface type | "url" |
| `address` | Video source address | YouTube URL, RTSP URL, file path |
| `video_dbms` | Database for video metadata | "customers" |
| `video_table` | Table for video data | "video_table" |
| `detection_dbms` | Database for detection results | "customers" |
| `detection_table` | Table for detection data | "detection_table" |
| `detection_column` | Object types to detect | "person", "car", "truck", "bus" |
| `recording_segment_time` | Video segment duration in minutes | 1, 5, 10 |
| `detection_ignore_time` | Seconds to ignore repeated detections | 10 |

### Detection Columns
Multiple detection columns can be specified to track different object types:
```
and detection_column = person
and detection_column = car
and detection_column = truck
and detection_column = bus
```

## Running the Video Stream

### Start Stream Command
```
run video stream 
  where name = <connection_name>
  and import_detect = <detection_function_name>
  and import_display = <display_function_name>
```

**Parameters:**
- `name`: Connection name (matches the name in video connect)
- `import_detect`: Detection function reference (e.g., "initiate_yolo")
- `import_display`: Display function reference (e.g., "imshow")

## Complete Example

```
# 1. Connect to database
connect dbms customers 
  where type = mongo 
  and ip = 127.0.0.1 
  and port = 27017 
  and user = demo 
  and password = passwd

# 2. Set video variables
video_url = "https://www.youtube.com/watch?v=rnXIjl_Rzy4"
video_host = 127.0.0.1
video_port = 8888

# 3. Enable detections
set enable_detections = true
set default_dbms = customers

# 4. Import display function
import function 
  where import_name = imshow 
  and lib = external_lib.video_processing.cv2_stream_imshow 
  and method = init_class

set function params 
  where import_name = imshow 
  and param_name = port 
  and param_type = int 
  and param_value = !video_port

set function params 
  where import_name = imshow 
  and param_name = host 
  and param_value = !video_host

# 5. Import detection function
import function 
  where import_name = initiate_yolo 
  and lib = external_lib.frame_modeling.yolo_detection 
  and method = init_class

set function params 
  where import_name = initiate_yolo 
  and param_name = module_type 
  and param_value = darknet

set function params 
  where import_name = initiate_yolo 
  and param_name = classes 
  and param_type = list 
  and param_value = []

set function params 
  where import_name = initiate_yolo 
  and param_name = module_path1 
  and param_value = /path/to/yolov4-tiny.weights

set function params 
  where import_name = initiate_yolo 
  and param_name = module_path2 
  and param_value = /path/to/yolov4-tiny.cfg

set function params 
  where import_name = initiate_yolo 
  and param_name = coco_path 
  and param_value = /path/to/coco.names

# 6. Create video connection
<video connect 
  where name = youtube
  and protocol = https
  and interface = url
  and address = !video_url
  and video_dbms = customers
  and video_table = video_table
  and detection_dbms = customers
  and detection_table = detection_table
  and detection_column = person
  and detection_column = car
  and detection_column = truck
  and detection_column = bus
  and recording_segment_time = 1
  and detection_ignore_time = 10
>

# 7. Run the stream
run video stream 
  where name = youtube
  and import_detect = initiate_yolo
  and import_display = imshow
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

## Required Libraries
- `av` (PyAV): Video/audio container handling
- `cv2` (OpenCV): Computer vision and display
- `numpy`: Array operations
- External detection libraries (e.g., YOLO/Darknet)

## Error Handling
The system includes comprehensive error handling for:
- Connection failures
- Library import issues
- Detection model errors
- Frame processing errors
- File write failures

## Statistics Tracking
The system tracks:
- Total frames processed
- Detections made
- Detections considered (after filtering)
- JSON files written (detection batches)