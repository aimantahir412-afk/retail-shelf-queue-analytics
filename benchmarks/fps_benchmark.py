
import time
import cv2

IMAGE_PATH = "samples/shelf_sample.jpg"

# Load the sample image
image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

# Benchmark basic image preprocessing
total_frames = 300
start_time = time.perf_counter()

for _ in range(total_frames):
    processed = cv2.resize(image, (960, 720))
    processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

elapsed_time = time.perf_counter() - start_time

fps = total_frames / elapsed_time

print("OpenCV Preprocessing Benchmark")
print("------------------------------")
print(f"Frames processed: {total_frames}")
print(f"Total time: {elapsed_time:.2f} seconds")
print(f"Processing FPS: {fps:.2f}")
