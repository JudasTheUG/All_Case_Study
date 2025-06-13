                                                 ###  READ ME ###

## Prerequisites

- Python 3.10+
- Google Chrome
- ChromeDriver/GeckoDriver (Explained in Detail on Step 2 of ## Set Up)

## Installation

1. Install the required Python packages:
    ```bash
    python -m pip install --upgrade pip
    python3 -m pip install virtualenv
    virtualenv -p python3 venv
    pip install selenium
    pip install -r requirements.txt
    ```

2. Download the appropriate ChromeDriver for your version of Chrome from [here](https://googlechromelabs.github.io/chrome-for-testing/)


## Set Up

1) Set up your environment so your code can run
    * Check interpreter, if not created automatically, Add python interpreter on the bottom right of the pycharm after opening the project


2)Handle chromedriver.exe issue
    a) For Local Runs Manually download compatible chromedriver/geckodriver from ## Installation Step 2 and put in root folder
        Sma4U_WebAutomation/
        │
        ├── README.md
        ├── .env.development
        ├── requirements.txt
        └── **chromedriver.exe**

    b) On local runs if driver download/update wanted to be automated(This is used in the case) 
        Just set "CHOSEN_BROWSER" as "chrome" or if you prefer firefox just put "any other text" but not chrome parameter
## Usage

To run the automation script, execute appropriate command from the below commands:

python <<py_file>>.py [<<py_file>> should be run_case(in this case) but the action Works genericly for all .py files]