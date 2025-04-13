# Model Usage Guide

Ensure the following files are in the correct folders:

- **Model Folder:**
  - `saved_model.pb`

- **Variables Folder:**
  - `variables.data-00000-of-00001`
  - `variables.index`

## Loading the Model

Use TensorFlow to load the model with:

```python
model = tf.saved_model.load('path_to_model_folder')
```