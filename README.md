# QtDraughts

Small program created as a student project back in uni. It implements MinMax algorithm used by ai opponent and uses python sockets for networking (multiplayer).
Documentation is generated in Sphinx, you can check it out [here](https://insopl.github.io/QtDraughts/html/index.html)
## Dependencies

For program to compile you need following libraries:
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt) - Gui and QtThread for multi threaded operations.
* [Pynacl](https://github.com/jedisct1/libsodium/) - Cryptography for network communication ]

## Creating single executable file

Executable files can be created using pyinstaller
There is pyinstaller's .spec file in main catalogue ("QtDraughts.spec") configured to export program to single executable file.
It was tested on:
* MacOS
* Windows 10
* Ubuntu 16.04

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
