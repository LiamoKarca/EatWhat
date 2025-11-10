# EatWhat
In our busy daily lives, choosing what to eat for each meal has become a common dilemma. With the pressure of work and life, and surrounded by countless restaurants and food options, people often struggle with the three big questions: “What should I eat for breakfast?”, “What should I eat for lunch?”, and “What should I eat for dinner?”

To address this problem, the system can capture restaurants that are currently operating in nearby locations and randomly select one to provide meal suggestions. It can also open Google Maps to show the restaurant’s location, helping users make quick and effortless dining decisions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Windows Executable for EatWhat](#windows-executable-for-eatwhat)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Installation

1. **Python**: Ensure Python is installed on your system.
2. **pip** (Python package installer): Make sure you have pip installed.

### Required Packages

- `beautifulsoup4`
- `playwright`
- `PyQt5`
- `PyQt5_sip`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage
Instructions on how to use the project, including code examples.

Run the project:

```bash
python main.py
```

After running `main.py`, a window titled 'EatWhat?' will appear, allowing you to interact with the corresponding buttons.


## Windows Executable for EatWhat

### Table of Contents

- [Prerequisites](#prerequisites)
- [Packaging the Project](#packaging-the-project)
- [Sharing the Executable](#sharing-the-executable)
- [Security Considerations](#security-considerations)


This guide explains how to package the EatWhat project into an executable (.exe) file for Windows operating systems. Follow these steps to create an executable version of the project using PyInstaller.

### Prerequisites

Before proceeding, ensure you have installed the `pyinstaller` package.

```bash
pip install pyinstaller
```

### Packaging the Project

1. **Modify main.spec File**: Make necessary modifications to the `main.spec` file based on the prompts provided within the file, especially adjusting file paths.

2. **Run PyInstaller**: Navigate to the directory containing `main.py` and execute the following command in the terminal:

    ```bash
    pyinstaller main.spec
    ```

3. **Locate Executable**: After running PyInstaller, two directories will be generated: `build` and `dist`. The `EatWhat.exe` file will be present within the `dist` directory.

4. **Run the Executable**: Double-click `EatWhat.exe` to launch the application.

### Sharing the Executable

If you want to share the executable with friends or family, consider the following recommendations:

- **Cloud Storage**: Upload the file to platforms like Dropbox for sharing. Avoid using Google Drive to prevent potential detection as a virus.
  
- **USB Drive**: Alternatively, share the file via USB drive and instruct the recipient to install it.

### Security Considerations

Before running the executable, ensure to take necessary security precautions to prevent false positives from Windows Defender:

1. **Exclude from Windows Defender**: Add the executable file to the exclusion list of Windows Defender to prevent it from being flagged as a virus.
   
   - Navigate to Windows Security > Virus & Threat Protection > Virus & Threat Protection Settings > Exclusions > Add or remove exclusions.

2. **Adjust Security Settings**: Modify Windows Security settings as needed to ensure smooth execution of the application.


## Contributing
If you'd like to contribute to this app development, feel free to fork this repository, make your changes, and submit a pull request. Please ensure your code follows the project's coding standards and includes appropriate documentation for any new features or changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact Information
If you have any questions or suggestions, please feel free to contact the project maintainer:

- **Email**: npustb11156057@gmail.com
- **GitHub**: [LiamoKarca](https://github.com/LiamoKarca), [LiYuTsen](https://github.com/Tsen01)

---
