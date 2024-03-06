# WinCuts

WinCuts is a Windows-native tool for easily setting up and managing custom keyboard shortcuts. It's designed for usage simplicity and is aimed at anyone who wants to save time and increase productivity by using keyboard shortcuts. 

## How it works

As of now, WinCuts lets you set up custom keyboard shortcuts for running shell/cmd commands that get launched whenever the shortcut is activated. It's useful if you need to launch specific commands frequently and want to save time by using a keyboard shortcut instead of typing the command every single time.

## Get WinCuts

### For Windows

Go to the [Releases](https://github.com/LyubomirT/wincuts/releases) page and download the latest version of WinCuts, typically we have a .zip file with all the binaries inside. Additionally, if you want full system-wide integration, you can install WinCuts using the provided installers.

### For Linux

Well, it's called `Win`Cuts for a reason (Windows-Cuts), but if you're ready to risk it, you can try running the source code downloaded either using a `.zip` file or by cloning the repository. **HOWEVER** I'm already planning to add switches for the tool to work on Linux (and probably Mac), so stay tuned.

### For Mac

Same as for Linux, but with a higher risk of not working at all.

### For Git

You can always clone the repository and build the project yourself, this is the recommennded way if you want to modify something before actually using the tool.

Specifically:

```bash
git clone https://github.com/LyubomirT/wincuts.git
cd wincuts
```

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

```bash
python wincuts.py
```

Tada! The app should be running if you've followed the steps correctly.

## Quickstart

After you've downloaded and installed WinCuts, you can start setting up your custom keyboard shortcuts. Simply enter the shortcut (keys separated with `+`), the command you want to run. If you need, you can toggle the Window Patch as well in case something doesn't work (varies for specific commands. For example, `chrome` won't work without the Window Patch, `notepad` doesn't even need it and so on).

> [!WARNING]
> Window Patch is experimental and might in fact break something, use it at your own risk.

### How to get rid of the window

Of course, many of us would like to have these shortcuts running in the background. That's why you can put the window in the system tray by simply closing it. If you want to close the app completely, you can right-click the system tray icon and select `Quit`.

Also, you can restore the window by clicking `Open` from the same menu.

### 
