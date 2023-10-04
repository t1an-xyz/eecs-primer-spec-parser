# EECS Primer Spec Parser
## Overview
Given a URL to an EECS specs spage using Primer Spec, parses the HTML and converts it
to a markdown file that you could use as a README in you GitHub repository.

## Usage
Download to python file from the repository.

Make sure to install BeautifulSoup and requests
```
$ pip install BeautifulSoup4
$ pip install requests
```

Run the program, providing the URL as a command line argument
```
$ python parse.py <URL>
```
> When adding the URL, make sure to include the `https://` at the beginning.

> Also make sure the docs directory does not exist or is empty before running the program.