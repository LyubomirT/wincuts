# WinCuts

WinCuts is a Windows-native (via Qt) tool for easily setting up and managing custom keyboard shortcuts. It's designed for usage simplicity and is aimed at anyone who wants to save time and increase productivity by using keyboard shortcuts. 

## How it works

As of now, WinCuts lets you set up custom keyboard shortcuts for running shell/cmd commands that get launched whenever the shortcut is activated. It's useful if you need to launch specific commands frequently and want to save time by using a keyboard shortcut instead of typing the command every single time.

What's also cool is that none of the shortcuts will go deep enough in your system to cause any damage. They're all running in the context of the user and are limited to the user's permissions. And, of course, the shortcuts are only active within the app and hence won't interfere with any other shortcuts you might have set up (basically, you can't accidentally override a system shortcut).

## Get WinCuts

Go to the [Releases](https://github.com/LyubomirT/wincuts/releases) page and download the latest version of the app. Afterwards, simply extract the contents of the archive and run the `wincuts.exe` file.

When the extraction is complete, it's recommended to go to the `integration` folder and run the `integration.exe` file. This will let WinCuts launch at startup and will make it easier to use.

### Uninstalling

No, you shouldn't just Shift+Delete the folder. Instead, you should go to the `integration` folder and run the `cleanup.exe` file. This will remove the startup integration and will make sure that nothing is left behind. Additionally, make sure to close the app (FROM THE SYSTEM TRAY) before running the cleanup.

Then you can delete the folder.

## Quickstart

After you've downloaded and installed WinCuts, you can start setting up your custom keyboard shortcuts. Simply enter the shortcut (keys separated with `+`), the command you want to run. If you need, you can toggle the Window Patch as well in case something doesn't work (varies for specific commands. For example, `chrome` won't work without the Window Patch, `notepad` doesn't even need it and so on).

> [!WARNING]
> Window Patch is experimental and might in fact break something, use it at your own risk.

### How to get rid of the window

Of course, many of us would like to have these shortcuts running in the background. That's why you can put the window in the system tray by simply closing it. If you want to close the app completely, you can right-click the system tray icon and select `Quit`.

Also, you can restore the window by clicking `Open` from the same menu.

### I don't want to run the app every time I start my PC

You should check out the [Get WinCuts](#get-wincuts) section and run the `integration.exe` file. This will make sure that WinCuts starts with your PC and you don't have to worry about it. It also makes sure that the app starts in the system tray without you having to do anything.

### Deleting a shortcut

That's not hard at all. Simply click the shortcut you want to delete and press the `Delete` button below the list. The shortcut will be removed and you won't be able to use it anymore. If you want to add it again, you'll have to do it manually.

## License

WinCuts is licensed under the BSD 3-Clause License. You can find the full license text in the `LICENSE` file in the root of the repository.

If you don't want to see that legal mumbo-jumbo, here's a quick summary:

- You can use WinCuts for whatever you want, as long as you don't claim that you made it and give credit to the original author.
- The author is not responsible for any damage caused by the software.
- You can't use the author's name to promote your own version of the software without permission.

## Contributing

Much appreciated! If you want to contribute, you can do so by forking the repository, making your changes and then creating a pull request. If you're not sure about something, you can always open a Discussion and ask for help.

## Support

If you need help with something, you can open a Discussion and ask for help. If you think you've found a bug, you can open an Issue and report it. If you want to suggest a feature, you can open a Discussion and suggest it.

Alternatively, you can try contacting me at Discord (`@lyubomirt`) or by email (`ternavski103@gmail.com`). I'll try to respond as soon as possible. 