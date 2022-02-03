The api automated tests for Migo.

**The tests require Python 3**

# HOWTOs

## Install on a local machine

 1. Clone repository.
    ```
    cd <projects_folder>
    git clone git@github.com:andrejew123/Migo.git
    cd Migo
    ```
 2. Create virtualenv and install requirements.
    ```
    python3 -m venv migo
    source migo/bin/activate
    pip install -r requirements.txt
    ```
 3. Add secrets file to Migo folder.
  
 4. To run all tests:
    ```
    python -m pytest test_1.py
    ```
    To specific test:
    ```
    python -m pytest -k "function_name"
    ```
    e.g:
    ```
    python -m pytest -k "test_put_invalid_body_checking_status_code_400"
    ```
   