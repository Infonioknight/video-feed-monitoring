# Real-Time Video Feed Monitoring for Safety and Security Compliance


## Table of Contents
 - [Project Overview](#project-overview)
 - [Dataset Documentation](#dataset-documentation)
 - [Model Selection and Training](#model-selection-and-training)
 - [Application on Video Feeds](#application-on-video-feeds)
 - []

## Project Overview

The core objective of the project will be to develop a system that is capable of real-time monitoring of designated areas using video feeds to ensure safety and security compliance.

## Example Video

https://github.com/Infonioknight/video-feed-monitoring/assets/44343059/c34b4a07-aca9-44e5-903e-4047f16e7267

### Key Components:
- Selection of a pre-trained base model.
- Dataset selection and modification to meet requirements.
- Transfer learning from pre-trained model on custom dataset.
- Application of trained model on video-feeds
- Implementation of Region of Interest (ROI)

## Dataset Documentation

### Original Dataset Information
- **Name:** Construction Site Safety Image Dataset Roboflow
- **Source:** [Construction Site Safety Image Dataset Roboflow](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow/data)
- **Description:** A dataset containing a great collection of construction site images which are annotated and labelled in the YOLO format. Most of the datasets are not annotated in this particular way, making this dataset very useful. This dataset has 10 different classes namely `{0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}`.

### Dataset Modification
- **Reason:** The original dataset had NON-person objects split into several separate classes and were streamlined in one single class. For this application, it is sufficient if the major classification for an object is either 'Person' or 'NON-Person'. There were also two classes that were deemed non-essential for this use-case and were therefore excluded.
- **Modification Process**: The code for the dataset modification can be found here [Dataset Modification](https://github.com/Infonioknight/video-feed-monitoring/blob/main/Code%20Notebooks/dataset-modification.ipynb). The aim of the above notebook is to edit the *labels* file (annotations) for each of the images in the dataset and change the classes according to the method mentioned above.

- **Changes:**
    - The original dataset had 10 different classes namely `{0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}` for object classification after detection.
    - This modified dataset has a total of 6 classes namely `{0: 'Hardhat', 1: 'NO-Hardhat', 2: 'NO-Safety Vest', 3: 'Person', 4: 'Safety Vest', 5: 'NOT-Person'}`.
    - It combines the classes `{6: 'Safety Cone', 8: 'machinery', 9: 'vehicle'}` into a single class named 'NOT-Person' and completely removes the classes `{1: 'Mask', 3: 'NO-Mask'}`.

- The dataset can be accessed and downloaded from the following link: [Construction Site Dataset v2](https://www.kaggle.com/datasets/gauravsekar/construction-site-safety-image-dataset-roboflow/data)

### Dataset Usage
- The original dataset was already well annotated and distinctly split into *Training*, *Validation* and *Test* sets. and covers a variety of possible cases and scenarios in Construction Site Safety.


## Model Selection and Training

### Pretained Model Selection
- **Model Chosen:** YOLOv8 (You Only Look Once Version 8)
- **Reasons:** By detecting objects directly, YOLOv8 skips time-consuming steps. Despite its speed, YOLOv8 maintains impressive detection accuracy and most importantly, it performs exceptionally well in scenarios with many objects and is also extremely easy to leverage.
- The documentation and model information can be found here: [YOLOv8](https://docs.ultralytics.com/)

### Training Process
- **Configuration**: The training process uses the following parameters defined.
    - Image Size (`imgsz`): 640 *(Resizes images to 640x640 px)*
    - Epochs (`epochs`): 30 *(Number of iteration through the dataset)*
    - Batch Size (`batch`): 32 *(Number of images processed in one cycle)*
- **Training Environment:** The model training was done on Kaggle after also performing EDA (Exploratory Data Analysis) on the dataset. Used PyTorch, *GPU T4 x 2*.
- **Steps:** 
    - Installed and imported necessary libraries and dependencies
    - Performed Exploratory Data Analysis on the dataset
    - Got all the image sizes and dimensions from the *train*, *test* and *validation* parts of the dataset.
    - Trianed model using the above configuration.
    - Sample predictions

- The link to the notebook used for training the model is in the following link: [Object Detection Training](https://www.kaggle.com/code/gauravsekar/object-detection/notebook?scriptVersionId=185699509)

- **Performance Metrics:** 
    - **F1 Score:** Maximum of **0.77** at a confidence threshold of **0.425**
    - **Mean Average Precision (mAP):** 0.791 at an IoU (Intersection over Union) threshold of 0.5 

## Application on Video Feeds

### Video Processing Pipeline
- **Inputs:** The current version of the code works using the live video feed obtained from a webcam. 
- **Preprocessing:** The video frames are extracted and resized to meet the model's required dimensions.
- **Inference:** Each of these frames are then passed through the model for object detection and obtaining the bounding boxes.

### Region of Interest Definition
- **Inputs:** The Region of Interest implementation has two main parts to it.
    - Marking the **boundary box** to be *visible on the interface when observing the video feeds*. This is used to **highlight the area** of the floor or region on the video-feed that is considered our region of interest.
    - Marking the **actual** Region of Interest. This is a box that is surrounds the **visible** boundary box. This takes into account the height of a person dimensions of their bounding box to make our detection work.
- **Implementation:** Each of the stages has a script which can be run and the points marked for the final prediction  and monitoring. The marked coordinates are stored and can be edited as required.

### Prediction and Output
- The boundary box is defined by marking the points on the video feed by the user.
- The Region of Interest is then defined by marking points on the video feed based off the boundary box determined. This Region of Interest must **surround** the initial boundary box and take into account:
    - Maximum height of the people that could appear in the given region
    - Extentions of the person's bounding boxes when standing at all extremities of the boundary box.
- When running the main program, the boundary box is in **GREEN** by default, siginifying that there are no threats at the moment.
- The model then predicts on the each frame of the video feed. If a **'Person'** class object is within the **boundary box**, the colour of the box changes from **GREEN** to **RED** signalling **DANGER**.

## Installation and Setup
