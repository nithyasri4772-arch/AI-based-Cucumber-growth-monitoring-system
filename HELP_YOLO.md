# 🧠 HELP: Optimal YOLO Creation Model

The most important part of your project: Teaching the AI to see cucumbers properly.

### 📜 Dataset Creation Strategy (Roboflow)
1.  **Project Name**: `Cucumber Harvest AI`
2.  **Image Quantity**: Aim for **30 to 50** photos for a start. 100+ is "Optimal".
3.  **Variations**:
    - **Angles**: Top, Side, and Close-up.
    - **Lighting**: Bright sun, Cloud, and Shadows.
    - **Occlusion**: Some photos where cucumbers are slightly behind leaves (this is where the fan helps!).

### 🚀 Annotation (Labeling) Rules
1.  **Label Name**: Use exactly `cucumber` (all lowercase).
2.  **Box Tightness**: Draw boxes as tight as possible to the fruit.
3.  **Missing Parts**: If a leaf covers a part of the cucumber, draw the box as if you can see the whole fruit.

### 💨 Training with the Fan
- When you capture your photos for training, use the **Fan on** to blow leaves.
- Capture photos during the "movement" so the AI learns what a cucumber looks like when leaves are waving.

### 📂 Deployment Path
1.  Click **Export** in Roboflow.
2.  Select **YOLOv8** format.
3.  After training on your PC using `TRAIN_MY_MODEL.bat`, the best model will be created.
4.  **MOVE IT TO**: `models/yolo/cucumber.pt`. 
5.  Set `vision: > use_mock_when_missing: false` in `settings.yaml`.

### 🎯 Accuracy Check
Open the **Dashboard** and look at the "AI Live View". If the green box is flickering, you need more photos in your dataset!
