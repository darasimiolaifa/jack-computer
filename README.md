# jack-computer

A collection of the software components of a simple computer system.

## Project Overview

The computer is a collection of many moving parts. Hardware that carry out instructions and softwares that tell the hardware what to do. To most people, the computer operates as a blackbox. It is a worthy project to take the machine apart and seek to build it together again. From scratch. Hence this project.

This repo is a collection of the software layers of a simple modern computer. A collection of an assembler, a virtual machine translator, and a compiler. All written in Python.

This project was inspired by (and is the result of doing the practical assignments of) the course "From Nand to Tetris", a pragmatic computer science course taught by Noam Nisan and Shimon Schocken on Coursera.

## Course Materials (code, tools, project files and instruction)

All the course resources (including tools to test generated files) and instructions can be found [here](https://nand2tetris.org)

## How To Set Up Locally

1. Make sure Python is installed on your system and the `pyhton` command is available in your terminal by setting it in your path
2. Clone this repo by typing in your terminal `git clone https://github.com/darasimiolaifa/jack-computer.git`
3. cd into the `jack-computer` folder. There should be four folders:

- `HackAssembler`
- `HackVMTranslator`
- `JackSyntaxAnalyzer`
- `JackOperatingSystem`.

4. cd into each folder and follow the instructions for each folder as stated in their section below.

### Hack Assembler

- While in the folder, run `python assembler Add.asm`. You should see a success message in your terminal and a `Add.hack` file created containing the translated code.

### Hack VM Translator

- While in the folder, run `python vm_translator Basic.vm`. You should see a success message in your terminal and a `Basic.asm` file created containing the translated code.

### Jack Sybtax Analyzer

- While in the folder, run `python syntax_analyzer Main.jack`. You should see a success message in your terminal and a `Main.vm` file created containing the translated code.

### Jack Operating System

- This folder contains the operating system code for the Jack computer.

## Alternative Testing

Alternatively, you could go top down in your testing, by running the `SyntaxAnalyzer` on the operating system folders, thereby generating vm code, then run your `VMTranslator` on that, generate the assembly code, and finally, run your `Assembler` on that to get your machine code.

## Author

Darasimi Olaifa
