import tensorflow as tf
import cv2

from dataclasses import dataclass

@dataclass
class Camera:
    focal_length:float # meters
    sensor_height:float # meters

class Drone:
    def __init__(self, y_min_relative, x_min_relative, y_max_relative, x_max_relative, image_width, image_height,
                 conf, camera:Camera, real_height_of_the_object):
        self.y_min_relative = y_min_relative
        self.x_min_relative = x_min_relative
        self.y_max_relative = y_max_relative
        self.x_max_relative = x_max_relative

        self.x_max_absolute = None
        self.y_max_absolute = None
        self.x_min_absolute = None
        self.y_min_absolute = None

        self.image_width = image_width
        self.image_height = image_height

        self.init_absolute_coords()

        self.conf = conf

        self.real_height_of_the_object = real_height_of_the_object

        self.camera = camera

        self.object_height = self.calculate_object_height()
        self.distance = self.init_distance()

    def init_absolute_coords(self):
        self.y_min_absolute = int(self.y_min_relative * self.image_height)
        self.x_min_absolute = int(self.x_min_relative * self.image_width)
        self.y_max_absolute = int(self.y_max_relative * self.image_height)
        self.x_max_absolute = int(self.x_max_relative * self.image_width)

    def init_distance(self):
        #                           focal length (m) * real height of the object (m) * image height (pixels)
        # distance to object (m) =     ----------------------------------------------------------------
        #                                           object height (pixels) * sensor height (m)
        return (self.camera.focal_length * self.real_height_of_the_object * self.image_height) / (self.object_height * self.camera.sensor_height)
    pass

    def calculate_object_height(self):
        fix = 0.9 # the boxes are slightly bigger than the drone
        return (self.y_max_absolute - self.y_min_absolute) * fix

class ObjectDetectionModel:
    def __init__(self, model_dir, focal_length, real_height, sensor_height):
        self.model_dir = model_dir
        self.focal_length = focal_length
        self.real_height = real_height
        self.sensor_height = sensor_height
        self.model = self.load_model(model_dir)

    @staticmethod
    def load_model(model_dir):
        try:
            model = tf.saved_model.load(model_dir)
            print("Model loaded successfully!")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    @staticmethod
    def preprocess_image(image):
        input_tensor = tf.convert_to_tensor(image, dtype=tf.uint8)
        input_tensor = input_tensor[tf.newaxis, ...]
        return input_tensor

    def make_predictions(self, input_tensor):
        detections = self.model(input_tensor)
        return detections

    @staticmethod
    def calculate_detections(drones):
        detections = []
        for drone in drones:
            detection = {
                'score': drone.conf,
                'startX': drone.x_min_absolute,
                'startY': drone.y_min_absolute,
                'endX': drone.x_max_absolute,
                'endY': drone.y_max_absolute,
                'distance': drone.distance
            }
            detections.append(detection)
        return detections

    @staticmethod
    def draw_detections(image, detections):
        for detection in detections:
            score = detection['score']
            startX, startY, endX, endY = detection['startX'], detection['startY'], detection['endX'], detection['endY']
            distance = detection['distance']

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

            label = f"Class Drone | Score: {score:.2f} | Distance: {distance:.2f} m"
            cv2.putText(image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image

    @staticmethod
    def process_predictions(drones, image):
        detections = ObjectDetectionModel.calculate_detections(drones)
        image = ObjectDetectionModel.draw_detections(image, detections)
        return image

    def retrieve_drone_data(self, detections, image, confidence_threshold=0.2):
        boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        camera = Camera(self.focal_length, self.sensor_height)
        drones = []
        for i in range(len(scores)):
            score = scores[i]
            box = boxes[i]
            if score >= confidence_threshold:
                ymin, xmin, ymax, xmax = box
                drone = Drone(ymin, xmin, ymax, xmax, image.shape[1], image.shape[0], score, camera, self.real_height)
                drones.append(drone)
        return drones

    def process_video(self, video_path, output_path=None, fps=30):
        cap = self._initialize_video_capture(video_path)
        if not cap:
            return

        out = self._initialize_video_writer(cap, output_path, fps)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = self._process_frame(frame)
            if processed_frame is None:
                continue

            if output_path:
                out.write(processed_frame)
            else:
                self._display_frame(processed_frame)

        self._finalize_resources(cap, out, output_path)

    @staticmethod
    def _initialize_video_capture(video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return None
        return cap

    @staticmethod
    def _initialize_video_writer(cap, output_path, fps):
        if not output_path:
            return None

            # Get frame width, height, and size
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (frame_width, frame_height)

        # Use H.264 codec (libx264) if supported, else fallback to MP4V
        try:
            # Attempt to use the H.264 codec
            #fourcc = cv2.VideoWriter_fourcc(*'H264')
            #fourcc = cv2.VideoWriter_fourcc(*'avc1')
            #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fourcc = cv2.VideoWriter_fourcc(*'X264')
        except Exception:
            print("H.264 codec not supported, falling back to MP4V")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Initialize the video writer
        return cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    def _process_frame(self, frame):
        try:
            input_tensor = self.preprocess_image(frame)
            detections = self.make_predictions(input_tensor)
            drones = self.retrieve_drone_data(detections, frame)
            return self.process_predictions(drones, frame)
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None

    @staticmethod
    def _display_frame(frame):
        cv2.imshow("Video - Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    @staticmethod
    def _finalize_resources(cap, out, output_path):
        cap.release()
        if out:
            out.release()
        else:
            cv2.destroyAllWindows()
        if output_path:
            print(f"Processed video saved to {output_path}")


#def main():
#    model_dir = "model"
#    video_path = "user_data/drone.mp4"
#    output_path = "processed_drone.mp4"

#    detection_model = ObjectDetectionModel(model_dir)
#    detection_model.process_video(video_path)


#if __name__ == "__main__":
#    main()
