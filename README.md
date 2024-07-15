# 1. Project Details:

* Topic: Microorganism Classification
* Goal: Creating an API that classifies JPG images of microorganisms and provides feedback with classification results and confidence levels.
* Data: Microorganism image dataset from Kaggle: https://www.kaggle.com/datasets/mdwaquarazam/microorganism-image-classification (8 classes: Amoeba, Euglena, Hydra, Paramecium, Rod_bacteria, Spherical_bacteria, Spiral_bacteria, Yeast)
* Deep Learning Model: Convolutional Neural Network (CNN)

# 2. Methodology

## Data Preprocessing

### Loading and Inspecting Data
- Images were loaded using `keras.preprocessing.image_dataset_from_directory` into batches of 32 and resized to 256x256 pixels.
- Data was inspected using Matplotlib subplots.

### Image Preprocessing
- Rescaling, resizing, flipping, and rotating were applied using TensorFlow Keras preprocessing functions.

### Data Splitting
- Data was split into 80% training, 10% validation, and 10% test sets before image processing.
- Input pipeline prefetching was used to enhance training performance.

# 3. CNN Architecture

### Model Structure
- **Image Preprocessing Layers:**
    - `resize_and_rescale`: Resizes images and rescales pixel values.
    - `data_augmentation`: Applies data augmentation techniques.
- **Convolutional Layers:**
    - 5 convolutional layers with 32, 64, 64, 64, and 64 filters (3x3 kernel sizes).
    - Each convolutional layer has a ReLU activation function.
- **Max-Pooling Layers:**
    - 5 max-pooling layers (2x2 pool size).
- **Dense Layers:**
    - Flattening layer.
    - Dense layer with 64 units and ReLU activation.
    - Final dense layer with 8 units (8 classes) and softmax activation.

## Training Process

### Training Setup
- TensorFlow and Keras libraries were used.
- GPU acceleration was utilized.

### Training Parameters
- Adam optimizer.
- Categorical cross-entropy loss function.
- 200 training epochs.
- Batch size of 32.

### Regularization
- Implicit regularization through data augmentation.

# 3. Results and Analysis

### Model Performance

#### Evaluation Metrics

- **Accuracy:**
    - Training accuracy: 91.99%
    - Validation accuracy: 89.06%
    - Typical confidence levels: Above 90%, often close to 99% for predictions.

### Visualizations

**Training Curves:**

![image](https://github.com/ShreyashCC/Micro-organism_Classification/assets/139590016/11a54f46-fb29-400b-887e-f0e1e1172364)

![image](https://github.com/ShreyashCC/Micro-organism_Classification/assets/139590016/5ff732c4-2a5b-42ad-8a4d-030bdde7d74a)



**Prediction and Confidence plots**

![image](https://github.com/ShreyashCC/Micro-organism_Classification/assets/139590016/3d69fa3e-eca5-454c-9754-32f0215a53f4)


* **Observations:**
    - Steady decrease in loss and consistent increase in accuracy throughout training.
    - Close alignment between training and validation curves suggests no overfitting.


# 4. API

## Framework and Server

* **Framework:** FastAPI
* **Web Server:** Uvicorn

## Endpoints

**`/ping` (GET):**
* Health check endpoint.
* Returns "hello I am alive" on success.

**`/predict` (POST):**
* Image classification endpoint.
* **Input:** Accepts a single image file as an `UploadFile` object.
* **Output:** Returns JSON response in the format:

```json
{
    "class": "Predicted class",
    "confidence": 0.95
}
