import random

class ObjectDetectionModel:
    def __init__(self):
        # In a real setup, load YOLO/EfficientDet model here
        self.classes = ["Poacher", "Animal", "Vehicle", "Ranger"]

    def predict(self, image_path):
        """
        Simulate object detection results.
        In real usage, run the deep learning model here.
        """
        num_objects = random.randint(1, 3)
        detections = []
        for _ in range(num_objects):
            obj_class = random.choice(self.classes)
            confidence = round(random.uniform(0.6, 0.99), 2)
            bbox = [random.randint(0, 100), random.randint(0, 100),
                    random.randint(100, 200), random.randint(100, 200)]
            detections.append({
                "class": obj_class,
                "confidence": confidence,
                "bbox": bbox
            })
        return detections


# ---------------- Demo Run ---------------- #
if __name__ == "__main__":
    model = ObjectDetectionModel()
    results = model.predict("test_image.jpg")
    print("Simulated detections:", results)
