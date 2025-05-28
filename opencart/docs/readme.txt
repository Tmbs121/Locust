# Prerequisites:

# 1). 
# I use BeautifulSoup Python library to parse html responses from OpenCart, so before running any Locust scripts, better check
# that BeautifulSoup is indeed installed in the virtual environment that I'm currently using
# (C:\Endava\EndevLocal\python_projects\Locust\.venv):

pip show bs4

# And if it shows it's not installed, install it:

pip install bs4
pip show bs4

# 2). 
# I also use lxml parser with BeautifulSoup library, so lxml needs to be installed in the same venv
# (C:\Endava\EndevLocal\python_projects\Locust\.venv):

pip install lxml


# 3).
# Install locust module in the same venv (C:\Endava\EndevLocal\python_projects\Locust\.venv):

pip install locust


# 4).
# Install pytest plugin in the same venv (C:\Endava\EndevLocal\python_projects\Locust\.venv):

pip install pytest


# 5).
# Install playwright module in the same venv (C:\Endava\EndevLocal\python_projects\Locust\.venv):

pip install playwright


# Alternatively, instead of steps 1 - 4, we can install everything (locust, bs4, lxml, playwright, pytest) in one go
# from requirements.txt file. To use requirements.txt file for modules installation:
# Add requirements.txt to LocustProject_1.
# Add to the file the list of all the modules that need to be installed:
	locust
	lxml
	bs4
	playwright 
	pytest
	
# No need to indicate the versions of the modules in the requirements file, the latest versions will be installed by default.

# Run requirements.txt from active virtual env (C:\Endava\EndevLocal\python_projects\Locust\.venv in this case) with the command:
pip install -r </path/to/requirements.txt>	


# 6).
# Once playwright module is installed, we also need to install all the browsers for it by running in the same venv:

playwright install

# NOTE: Even with all the above steps completed, running pytest files ocassionally gives an error: fixture 'page' not found.
# And the error makes a reference to the lines of code where our pytest functions are defined with the corresponding fixtures,
# like: def test_go_to_home_page(page: Page) for example.
# If that's the case, we can try to install the pytest wrapper pytest-playwright that provides default support for fixtures
# for all the browsers that had been installed for playwright in the step 6. To install the pytest wrapper, just run:

pip install pytest-playwright
   
 
______________________________________________________________________________________________________________________________

Commands for non-GUI mode (running the test in the terminal only):

# The command below starts the test in headless mode with 5 users, spawn rate of 1
# -i option here is supposed to define the number of iterations for each task, so if want to run each task only a certain
# number of iterations rather than run the test endlessly until it's stopped by Ctrl+C, we may want to include the -i
# option in the command. However, -i doesn't seem to work with SequentialTaskSet the way I expected. 
# It just repeats the first sub-task in the SequentialTaskSet and never gets to run the rest of the sub-tasks:

locust -f locust-api/compare_products.py --headless -u 5 -r 1 -i 4


# Another example of the Locust command to start the test in non-GUI.
# This version runs the python file which includes SequentialTaskSet class. 
# Make sure your current location is LocustProject_1 !
 
locust -f locust-api/compare_products.py --headless --run-time 120s -u 2 -r 1

# Command to run a Locust test using GUI mode (GUI window appears allowing to set the parameters of the test and control the run):
locust -f locust-api/compare_products.py

# Local Locust instance runs in the browser on localhost:8089

# Commands to run a .py file (with pytest plugin!) in Debug mode to pull up a Playwright inspector on the screen.
# This is to be run from your IDE integrated terminal.
# Before running the pytest command, make sure your current location is `opencart` package because that's where
# test_data\opencart_creds.csv file is located. Trying to run the test from a location other than `opencart`
# will return an error saying `opencart_creds.csv` file cannot be found.  

cd opencart
.venv\Scripts\activate
$env:PWDEBUG=1
pytest -s


# Commands to run a .py file without pytest plugin in Debug mode to pull up a Playwright inspector on the screen.
# This is to be run from your IDE integrated terminal:

cd opencart
.venv\Scripts\activate
$env:PWDEBUG=1
python playwright-ui/compare_products_std_playwright.py
________________________________________________________________________________________
# REPL mode guidance:

# Playwright for Python has the so-called REPL mode which is an interactive mode that allows us to execute the script code
# in real time line by line and see the effect of each line of code being executed in a separate browser window.
# That's handy while creating a script because instead of writing the whole script first and then running
# the whole thing and trying to find a problematic piece of code if smth doesn't work as expected we can instead
# execute our script step by step as we add each new line of code, so if smth is off in the specific line of code
# we will spot it immediately.

# To enter the interactive REPL mode we need to activate the virtual environment in the terminal first:
cd opencart
.venv\Scripts\activate
# and then just type the python command:
python
# This will get us into the interactive playwright mode and the terminal will show us we are in the REPL mode by
# displaying >>> (triple right arrows) at the start of each terminal line.
# Once we get into the REPL mode we'd need to write a few lines of code to initiate the objects/instances that are
# mandatory to be initiated for each playwright test, so we'd go:
# >>> from playwright.sync_api import sync_playwright
# >>> playwright = sync_playwright().start()
# >>> browser = playwright.chromium.launch(headless=False, slow_mo=500)
# >>> page = browser.new_page()
# >>> page.goto("http://172.23.176.159/opencart/upload")
# >>> signin_link = page.get_by_role("link", name="Login")
# >>> We can highlight the web element we need (signin link in this case) to make sure that's indeed the element we want:
# >>> signin_link.highlight()
# >>> Now we are good to proceed with the rest of our script according to our UI flow. 

# To quit the REPL mode, we'd first need to close the browser and stop the playwright instance and then exit REPL session:
# >>> browser.close()
# >>> playwright.stop()
# >>> exit()

# And now we are out of REPL and back to the usual mode in the terminal, in the active venv.
_____________________________________________________________________________________________

# To start playwright in recording mode, run from the terminal:
playwright codegen

# We can also start codegen indicating the URL address of the website that we want to record our actions on, right in the command:
playwright codegen http://172.23.176.159/opencart/upload/ 

# We can also add to the same command the path to the file where we want playwright inspector to save the recorded code.
playwright codegen http://172.23.176.159/opencart/upload/ -o <path to the file>