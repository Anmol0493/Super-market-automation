# Automated Web Ordering System

This project consists of Python scripts for automated ordering from two different websites: PriceSmart and Loshusan Supermarket. It utilizes Selenium for automation tasks.

## Prerequisites

Before running this script, make sure you have the following prerequisites installed:

- **Python**: Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- **Selenium**: Install Selenium using pip:

    ```bash
    pip install selenium pandas
    ```

- **Chrome WebDriver**: If any issue occures in opening webdriver, just update selenium and system's chrome.

## Usage

1. Clone or download this repository to your local machine.

2. Install the necessary Python libraries mentioned in the Prerequisites section.

3. Make sure you have the Chrome WebDriver executable file in your PATH or specify its location in the script.

4. Create a `userconfig.txt` file in the root directory. This file is crucial for configuring the script to automate from specific websites and handle user authentication.

5. The `userconfig.txt` file format is as follows:

    ```
    [WEBSITE]-[LOCATION]-[FILENAME]/[USERID]/[PASSWORD]/[ORDER_NUMBERS]
    ```

    - `[WEBSITE]`: Currently supported websites are `PriceSmart` and `Loshusan`.
    - `[LOCATION]`: Location information (if applicable).
    - `[FILENAME]`: Name of the input CSV file containing product details.
    - `[USERID]`: Username or email address required for website authentication.
    - `[PASSWORD]`: Password required for website authentication.
    - `[ORDER_NUMBERS]`: Optional comma-separated list of order numbers to filter products.

6. Run the main script `main.py`:

    ```bash
    python main.py
    ```

7. The script will save product information and save the output to an `output.csv` file.

## Additional Notes

- Ensure the Chrome WebDriver executable path is correctly set in the script.
- Customize the automation logic in the `pricemart.py` and `loshusansupermarket.py` files as needed.
- Handle exceptions and error scenarios gracefully to ensure robustness of the script.
- Regularly update the `userconfig.txt` file to specify the correct input files and authentication details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
