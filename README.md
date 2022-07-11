# Royal Road Scraper
## Summary
*RRScraper* is a minimalistic web-scraper with basic HTML/CSS handling and management features for the novel self-publishing website [*Royal Road*](https://www.royalroad.com/home).

This software came to be after having had a long flight a couple weeks back with no Wi-Fi, and lamenting not having stored a couple chapters for offline reading.

# Setup & Usage:

## Setup:
This is a simple *Python* script - as such, it can either be run from ta command-line interface, IDE or Python interpreter. (One can also build it into an executable if desired).

## Requirements

As mentioned, the software is both written in *Python*, and relies on a small set of *Python* libraries. Due to this, having *Python* installed in your system is a **must**. 

It is advised to set up a Python virtual environment to contain the project as to avoid any potential conflicts with global library installations. For this, after forking the repository, the following command can be executed within the project directory for creating a local virtual environment:
```powershell
> python -m venv .venv                        # Create a virtual env. in a subfolder named '.venv'
```

Once the virtual environment has been created, it must be activated and the required Python libraries install. This can be done through *Pip* by making usage of the provided [*requirements.txt*](requirements.txt) file with the following command:
```powershell
> .venv/Scripts/Activate.ps1                  # Activate the virtual environment
> python -m pip install -r requirements.txt   # Install the libs. listed in 'requirements.txt'
```

## Usage:
Once everything is set up and the dependancies installed, one can run the program from within the virtual environemnt by simply executing the main script, [*RRScraper.py*](RRScraper.py). A glance at the help menu from a *PowerShell* powershell is shown below:
```powershell
(.venv) PS> X:\RoyalRoadScraper> python .\RRScraper.py --help
usage: RRScraper.py [-h] -n NAME -l LINK [-l RANGE] [-o OUT] [-v]

Scrape Novels from RoyalRoad.
optional arguments:
  -h, --help            show this help message and exit

Required Arguments:
  -n NAME, --name NAME  Novel's name
  -l LINK, --link LINK  Link to the novel's index

Optional Arguments:
  -l RANGE, --range RANGE Range of chapters to scrape
  -o OUT, --out OUT     Output directory
  -v, --verbose         Execute in verbose mode
```

- The ***name*** argument specifies a novel name to be used internally by the script (i.e. in verbose mode and default folder creation). If the name has spaces, make sure to wrap it in quotation marks.

- The ***link*** argument specifies the novel's frontpage from which to scrape the respective chapter table. The link can be given in either full-form ("www.royalroad.com/fiction/#/novel-name") or short-handed form (i.e. "/fiction/#/novel-name").

- The ***range*** argument specifies a range of chapters to scrape. The format for the argument should be N1-N2, where N1 < N2 (i.e. 1-100, 25-25, etc.). Note that the chapter number might not match the chapter index position since authors sometimes publish polls/announcements/alternative POVs/etc. If the range is not specified, the entire available range will be scraped. Single chapters can be specified as N-N (i.e. 20-20)

- The ***output*** argument specifies a subfolder into which the chapters will be stored. If no output folder is specified, the default will be Novels/[Novel Name]/ in the project's directory.

- The ***verbose*** argument specifies whether the program should output status messages as it runs.

## Example Commands
Some command examples following the format specified above:

```powershell
> RRScraper.py -n "Novel Name" -l /fiction/123/novelname
> RRScraper.py --name "Novel Name" --link /fiction/123/novelname --out Folder
> RRScraper.py -n "Novel Name" -l https://www.royalroad.com/fiction/123/novel-name -v
> RRScraper.py -n "Novel Name" -l https://www.royalroad.com/fiction/123/novel-name -o Folder -v
> RRScraper.py -n "Novel Name" -l https://www.royalroad.com/fiction/123/novel-name -r 1-100 -o Folder -v
> RRScraper.py -n "Novel Name" -l /fiction/123/novel-name -range 21-73 -o Folder -v
```


If run with the *verbose* argument, the program will output status updates as it executes: 

![Script Execution](Images/Execution.png)

You should then have a folder created within the Novels/[Output] subdirectory with the the scraped chapters.

![Script Result](Images/Result.png )

# Notes

- The scraper enforces a 1 second delay inbetween each chapter download. This is to not spam the RoyalRoad servers. One can reduce (or even remove) this delay if desired within the sourcecode, but I would strongly encourage you not to.

- The stored chapters are saved as HTML files, and make use of a very simple CSS file which can be found under [*Templates/ChapterCSS.css*](Templates/ChapterCSS.css). Feel free to tweak said file to customize you reading experience.

- Remember to support [RoyalRoad](https://www.royalroad.com/home "RoyalRoad") and its authors, as well as to be polite when saving chapters for offline reading.