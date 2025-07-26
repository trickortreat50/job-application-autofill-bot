# Conda Environment Setup for Job Application Auto-Fill Bot

This guide will help you set up the Job Application Auto-Fill Bot using conda.

## Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed
- Google Chrome browser installed
- Windows, macOS, or Linux

## Step-by-Step Setup

### 1. Open Terminal/Command Prompt

**Windows:**
- Open Anaconda Prompt (from Start Menu)
- Or open Command Prompt and activate conda

**macOS/Linux:**
- Open Terminal

### 2. Navigate to Project Directory

```bash
cd "path/to/your/Resume Tailor"
```

### 3. Create Conda Environment

```bash
conda env create -f environment.yml
```

This will create a new conda environment named `job-auto-fill` with all required dependencies.

### 4. Activate the Environment

```bash
conda activate job-auto-fill
```

You should see `(job-auto-fill)` at the beginning of your command prompt.

### 5. Verify Installation

```bash
python --version
pip list
```

You should see Python 3.9 and all the required packages listed.

### 6. Configure Your Information

Edit the `config.py` file with your personal information:

```bash
# On Windows
notepad config.py

# On macOS/Linux
nano config.py
# or
code config.py  # if you have VS Code
```

Replace all placeholder information with your actual details.

### 7. Run the Application

**GUI Mode (Recommended):**
```bash
python main.py
```

**Command Line Mode:**
```bash
python main.py --cli
```

## Environment Management

### Activate Environment (Every Time You Use the Bot)
```bash
conda activate job-auto-fill
```

### Deactivate Environment
```bash
conda deactivate
```

### Update Environment (If You Pull New Changes)
```bash
conda env update -f environment.yml
```

### Remove Environment (If You Want to Start Over)
```bash
conda env remove -n job-auto-fill
```

## Troubleshooting

### Environment Creation Fails
If you get errors creating the environment:

1. **Update conda:**
   ```bash
   conda update conda
   ```

2. **Try creating with pip dependencies separately:**
   ```bash
   conda create -n job-auto-fill python=3.9 selenium=4.15.2 webdriver-manager=4.0.1 pyperclip=1.8.2
   conda activate job-auto-fill
   pip install keyboard==0.13.5 tkinter-tooltip==2.0.0
   ```

### Chrome Driver Issues
If you get Chrome driver errors:

1. **Make sure Chrome is installed and up to date**
2. **Try updating the environment:**
   ```bash
   conda activate job-auto-fill
   pip install --upgrade webdriver-manager
   ```

### Package Conflicts
If you have package conflicts:

1. **Remove and recreate the environment:**
   ```bash
   conda env remove -n job-auto-fill
   conda env create -f environment.yml
   ```

## Alternative: Manual Environment Creation

If the `environment.yml` doesn't work, you can create the environment manually:

```bash
# Create environment
conda create -n job-auto-fill python=3.9

# Activate environment
conda activate job-auto-fill

# Install conda packages
conda install -c conda-forge selenium=4.15.2 webdriver-manager=4.0.1 pyperclip=1.8.2

# Install pip packages
pip install keyboard==0.13.5 tkinter-tooltip==2.0.0
```

## Environment Information

The conda environment includes:
- **Python 3.9** - Programming language
- **Selenium 4.15.2** - Web browser automation
- **webdriver-manager 4.0.1** - Automatic Chrome driver management
- **pyperclip 1.8.2** - Clipboard operations
- **keyboard 0.13.5** - Keyboard input handling
- **tkinter-tooltip 2.0.0** - GUI tooltips

## Next Steps

After setting up the conda environment:

1. **Configure your information** in `config.py`
2. **Test with a simple job application**
3. **Read the main README.md** for usage instructions
4. **Start applying to jobs more efficiently!**

## Notes

- The conda environment keeps your project dependencies isolated
- Always activate the environment before running the bot
- You can have multiple conda environments for different projects
- The environment file ensures consistent setup across different machines 