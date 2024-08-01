# Lenovo Warranty Checker
## Description
This project consists of two scripts, `LenovoWarantyOne.py` and `LenovoWaranty.py`, designed to interact with Lenovo's API to retrieve product and warranty information based on serial numbers. The `LenovoWarantyOne.py` script processes a single serial number provided as a command-line argument, while `LenovoWaranty.py` processes multiple serial numbers from a CSV file and updates the CSV with the retrieved information.

## Requirements
- Python 3.x
- `requests` library

You can install the `requests` library using pip:
```sh
pip install requests
```

## Files
### 1. LenovoWarantyOne.py
This script fetches and displays product and warranty information for a single Lenovo product based on its serial number.
```sh
python LenovoWarantyOne.py <serial_number>
```

### 2. LenovoWaranty.py
This script processes a CSV file of Lenovo serial numbers, fetches the corresponding product and warranty information, and updates the CSV file with this information.
```sh
python LenovoWaranty.py <csv_file_path>
```

### template.csv
This file has a template structure that `LenovoWaranty.py` expects.

## Contributing
We welcome contributions to this project! If you have suggestions for improvements, new features, or bug fixes, please follow the steps below:

1. **Fork the Repository:**
   - Click on the "Fork" button at the top of this repository page to create a copy of the repository in your GitHub account.

2. **Clone Your Fork:**
   - Clone your forked repository to your local machine.

3. **Create a Branch:**
   - Create a new branch for your changes:
     `git checkout -b feature/your-feature-name`

4. **Make Your Changes:**
   - Modify the code and add your improvements or new features.

5. **Commit Your Changes:**
   - Commit your changes with a descriptive commit message:
    `git commit -m "Description of your changes"`

6. **Push to Your Fork:**
   - Push your changes to your forked repository:
    `git push origin feature/your-feature-name`

7. **Create a Pull Request:**
   - Go to the original repository and click on the "Pull Requests" tab.
   - Click on the "New Pull Request" button and select your branch from the dropdown menu.
   - Provide a descriptive title and detailed description of your changes.
   - Click on the "Create Pull Request" button.

We will review your pull request and provide feedback or merge it into the main branch. Thank you for your contributions!