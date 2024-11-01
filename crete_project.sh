#!/bin/bash

mkdir -p noise_cancellation/{domain,application,infrastructure,interface,tests}

touch noise_cancellation/domain/__init__.py
touch noise_cancellation/domain/models.py
touch noise_cancellation/domain/services.py

touch noise_cancellation/application/__init__.py
touch noise_cancellation/application/use_cases.py

touch noise_cancellation/infrastructure/__init__.py
touch noise_cancellation/infrastructure/audio_io.py
touch noise_cancellation/infrastructure/device_manager.py
touch noise_cancellation/infrastructure/noise_reduction.py

touch noise_cancellation/interface/__init__.py
touch noise_cancellation/interface/main.py

touch noise_cancellation/tests/__init__.py
touch noise_cancellation/tests/test_domain.py
touch noise_cancellation/tests/test_application.py
touch noise_cancellation/tests/test_infrastructure.py
touch noise_cancellation/tests/test_interface.py

touch noise_cancellation/requirements.txt
touch noise_cancellation/README.md

echo "Project structure created successfully."
