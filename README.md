# B01004283_EGM722
Overview
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
B01004283_EGM722 is a python-based project designed to generate maps of counties in Northern Ireland (NI). The project allows the user to specify which NI county they would like to map and to save the map if they wish. The user can choose to select all counties, at which point the project generates a map covering the whole NI region.
The project primarily utilises the shapely, matplotlib, geopandas, and cartopy python packages, for processing the project datasets and generating the map figures. 
The GitHub repository includes the relevant datasets required to run the project. These are contained in the ‘data_files’ folder. All the utilised datasets are in the form of ESRI Shapefiles (.shp). No additional datasets are required to run the project.

For guidance on using the project, please refer to the user guide.

Setup
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
To run the project, it is recommended that you download and install the following software tools:
    
    Integrated development environment (IDE): PyCharm Community Edition(or Professional Edition if you already have access)
   
    Conda environment and package manager: Anaconda Navigator
    
Note that other IDEs and conda management tools are available, however the instructions in this document will only detail set-up using PyCharm and Anaconda Navigator.
As this project is stored as a GitHub repository, it is highly recommended that you install Git, create a GitHub online account, and install GitHub desktop.

1 Linking the project to your GitHub account
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
If you are using Git and GitHub, please follow the below instructions for obtaining the project files. (If you are not using Git and GitHub, refer to Section 2).

On GitHub Online, navigate to the B01004283_EGM722 repository. From here, select the Code tab on the navigation bar.
You now need to create a forked copy of the repository, which will be linked to your individual GitHub account. To do this, at the top right of the Code tab, select Fork.
On the next window, enter an appropriate Repository name and optional Description. Then select Create fork. The forked copy with then be added to your list of repositories.
You now need to clone your repository to GitHub Desktop. To do this, open GitHub Desktop and log into your GitHub account. From the home screen, go to File and then Clone repository.
In the pop-out window, select your newly forked repository, choose a suitable file location to store your local version, and select Clone.

2 Downloading project files without a GitHub account
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
On the Code tab of the project GitHub repository, select the green Code button and then Download ZIP. You should then extract the repository files to a suitable location.

3 Creating the conda environment
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
To complete this step, you will need to ensure that you have downloaded and installed Anaconda Navigator, or a similar conda environment manager.

Open Anaconda Navigator and select the Environments tab. At the bottom of this tab select Import. In the Import Environment pop-out window, under Local Drive, import the environment.yml file from your cloned repository folder. Provide a suitable name for your conda environment and select Import.

4 Creating PyCharm project
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
You will need to setup your PyCharm Project. Once you have downloaded and installed either PyCharm Community or Professional Edition, create a New Project.

In the New Project pop-out window, select the folder of your cloned repository as the Location.
Select Custom environment as the Interpreter type. Select the Type as Conda. Select the path to your conda environment manager, in this case Anaconda Navigator. Under the Environment drop-down, select the conda environment that you created in Section 3. Now select Create to generate the PyCharm project.

5 Linking PyCharm Terminal
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Next, you need to ensure that your PyCharm Terminal is linked your conda environment. Go to File, Settings, and then in the pop-out window, Tools then Terminal. 

On the Terminal tab, ensure that the Shell Path is in the following format:
cmd.exe /K [conda location]\Scripts\activate.bat [conda location]

The [conda location] should be the file path to your conda environment manager, for example: C:\User\Example\anaconda3
Once you have updated the Shell Path select OK to close the window.
Now open the Terminal window itself, and check that your project conda environment is activated. If not use the following command to activate the correct environment:
conda activate B01004283_EGM722

B01004283_EGM722 in the command above should be replaced with the name you have given to the conda environment.

6 Setting up PyCharm Interpreter
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Next, to set-up the PyCharm interpreter, go to File, Settings, Project: B01004283_EGM722, Python Interpreter, Add Interpreter, Add Local Interpreter.

On the pop-out window, for Environment choose Select Existing. Select the Type as Conda. Ensure the Path to Conda is the location of your conda environment manager and the second Environment field is set as your conda environment.

7 Setting up PyCharm Run/Debug Configuration 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Finally, you need to create your Run / Debug Configuration. Open the Project _RUN_ME.py and next to the play button in the top right, select Edit Configuration.

In the pop-out window, under Run, select your conda environment. Under the Working directory, select the primary project folder and then select OK.
