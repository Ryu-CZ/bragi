# Bragi

Bragi is a custom real-time noise cancellation application designed to filter out background noises like PC fans, squeaking chairs, keyboard typing, and mouse clicks from your microphone input. It leverages machine learning to adapt to your unique voice characteristics, especially suited for voices with a wide frequency range.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Training Your Model](#training-your-model)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Real-Time Noise Cancellation**: Applies noise reduction on microphone input in real-time.
- **Customizable**: Train your own noise reduction model tailored to your voice and environment.
- **Virtual Microphone**: Creates a virtual microphone that can be used by any application.
- **Modular Architecture**: Built using the Onion Architecture for maintainability and scalability.

---

## Architecture

Bragi is structured using the Onion Architecture, promoting a clear separation of concerns:

- **Domain Layer (`domain/`)**: Contains core business logic and domain models.
- **Application Layer (`application/`)**: Orchestrates use cases by coordinating domain and infrastructure layers.
- **Infrastructure Layer (`infrastructure/`)**: Implements interfaces and interacts with external systems.
- **Interface Layer (`interface/`)**: Entry point of the application; handles user interactions.

---

## Installation

### **Prerequisites**

- **Operating System**: Linux (tested on Ubuntu 20.04)
- **Python**: Version 3.6 - 3.8 (to ensure compatibility with TensorFlow 2.x)
- **Audio Libraries**:
  - `portaudio19-dev`
  - `pulseaudio`
  - `pavucontrol` (for managing audio devices)

### **Step-by-Step Guide**

1. **Create the Project Directory**

   ```bash
   mkdir bragi
   cd bragi
   
2. **Set Up the Project Structure**

    Follow the Project Structure guidelines to create the necessary directories and files.

3. **Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```


4. **Install Dependencies**

```bash
pip install -r requirements.txt
```
5. **Install System Dependencies**
```bash
sudo apt-get update
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install pulseaudio pavucontrol
```

5. **(Optional) Initialize Git Repository**

```bash
git init
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
git add .
git commit -m "Initial project setup"
```

## Usage
1. **Configure the Application**

Edit `config.py` to ensure that device names and model paths are correctly specified.

2. **Provide or Train a Noise Reduction Model**

Place your trained model in the `models/` directory specified in `config.py` (default is `models/noise_reduction_model.h5`).

3. **Run the Application**

```bash
python interface/main.py
```

4. **Set Up the Virtual Microphone**

* Open PulseAudio Volume Control:

```bash
pavucontrol
```

 * Navigate to the Recording or Input Devices tab.

* Locate `VirtualMic` or `Monitor of VirtualMic` and set it as the input source for your applications.

5. **Configure Applications to Use Bragi**

In your application's audio settings (e.g., Zoom, Discord), select `VirtualMic` or `Monitor of VirtualMic` as the microphone input.

### Configuration

Create a `config.py` file in the root directory with the following content:

```python
class Config:
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    INPUT_DEVICE_NAME = 'YourMicrophoneName'
    OUTPUT_DEVICE_NAME = 'VirtualMic'
    MODEL_PATH = 'models/noise_reduction_model.h5'
```

* SAMPLE_RATE: The audio sampling rate.
* CHUNK_SIZE: Number of samples per audio chunk.
* INPUT_DEVICE_NAME: Name of your physical microphone (use list_audio_devices.py to find the exact name).
* OUTPUT_DEVICE_NAME: Name of the virtual microphone sink.
* MODEL_PATH: Path to your trained noise reduction model.

## Training Your Model
To train your own noise reduction model:

1. Collect Data

Record clean voice samples in a quiet environment using your microphone.
Record noise samples (e.g., PC fans, keyboard typing).
Mix clean voice and noise samples at various SNR levels using audio processing tools or scripts.

2. Preprocess Data

Standardize sampling rates (e.g., 16 kHz).
Extract features (e.g., spectrograms) using libraries like `librosa`.

3. Train the Model

Use machine learning frameworks like `TensorFlow` or `PyTorch`.
Follow tutorials or guidelines for training speech enhancement models.
Save the trained model to the path specified in config.py.

4. Integrate the Model

Ensure the model is correctly loaded in `infrastructure/noise_reduction.py`.

## Testing
Run unit tests to ensure each component works correctly.


```bash
python -m unittest discover tests
```

Ensure that your tests are properly configured and located within the tests/ directory.

Troubleshooting
No Sound Output

Verify that the virtual microphone is created and selected in both pavucontrol and your application.
Check if your physical microphone is correctly specified in config.py.
High Latency or CPU Usage

Optimize your model for real-time inference (e.g., use a smaller model, apply quantization).
Ensure your system meets the necessary hardware requirements.
Errors on Startup

Confirm that all dependencies are installed and compatible with your Python version.
Check for typos or incorrect device names in config.py.
Virtual Microphone Not Detected

Ensure pulseaudio is running.
Check that the virtual microphone module is loaded (restart the application if necessary).
Contributing
Contributions are welcome! Please follow these steps:

Fork the project repository.

Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
Commit your changes with clear messages:
```

```bash
git commit -m "Add your message here"
```
Push to your forked repository:

```bash
git push origin feature/your-feature-name
```

Submit a pull request to the original repository.

## License
This project is licensed under the MIT License. See the LICENSE file in the project root for details.


