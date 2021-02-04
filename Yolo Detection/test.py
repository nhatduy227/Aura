from pathlib import Path
base_path = Path(__file__).parent
weights_path = str(base_path) + "/pretrained models/yolov3.weights"

print(weights_path)