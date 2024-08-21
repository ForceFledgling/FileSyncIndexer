# FileSyncIndexer

A Python utility for indexing and syncing files from multiple directories, ensuring only fully downloaded or copied files are processed.

## Overview

FileSyncIndexer is a Python script designed to index files from specified directories and copy them to a temporary directory while preserving the folder structure. The script ensures that files are only processed after they have been fully downloaded or copied.

## Features

*   Indexes files from multiple directories.
*   Copies files to a temporary directory, preserving the folder structure.
*   Skips files that are still being downloaded or copied.
*   Automatically updates the index with new files.

## Requirements

*   Python >= 3.6

## Installation

1\. Clone the repository:

```
git clone https://github.com/ForceFledgling/FileSyncIndexer.git
```

2\. Navigate to the project directory:

```
cd FileSyncIndexer
```

## Usage

1\. Customize the directories to be indexed by modifying the source\_dirs list in the script.

2\. Run the script:

```
python3 indexer.py
```

3\. On the first run, the script will create a file index without copying any files. On subsequent runs, if the `index.json` file already exists, the script will check and update the index, then copy any new files to the specified temporary directory.

## Running in Background

To run the script in the background, you can use screen:

```
screen -S FileSyncIndexer
python3 indexer.py
```

To detach from the screen session, press Ctrl + A followed by D.

## License

This project is licensed under the MIT License.

## Contributions

Feel free to open issues or submit pull requests to improve the project.