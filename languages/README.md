# Languages

If you want to remove a language from the bot or add a new one, just delete or create a .json file following the instructions at the "Adding a language" section of this README.md.

## Supported languages

This is the list of directly supported languages in the bot, the names it can be called under and the tools that he uses to run the code of said language (and thus, they should be installed in your local machine.)

- C: It uses `gcc` to compile the code. You can use this language by calling it `c`.
- C++: It uses `g++` to compile the code. You can use this language by calling it `c++` or `cpp`.
- Rust: It uses `rustc` to compile the code. You can use this language by calling it `rust` or `rs`.
- Bash: It uses `bash` to run the code. You can use this language by calling it `bash` or `sh`.
- Python: It uses `python` to run the code. You can use this language by calling it `python`, `python3`, `py` or `py3`.
- Javascript: It uses `nodejs` to run the code. You can use this language by calling it `javascript` or `js`.
- Go: It uses `go run` to run the code. You can use this language by calling it `go`.
- Guile: It uses `guile` to run the code. You can use this language by calling it `guile`.
- Racket: It uses `racket` to run the code. You can use this language by calling it `racket` or `rkt`.
- R: It uses `rscript` to run the code. You can use this language by calling it `r`.
- Dart: It uses `dart` to run the code. You can use this language by calling it `dart`.
## Adding a language

In order to add a language to the bot, you have to create a filed calle `LANGNAME.json` inside this folder, replacing `LANGNAME` by the name of the language you want to add. Then, edit the .json file with your text editor of choice, and add the following template, replacing the vaules accordingly. There's an explanation for each value at the bottom.

```json
{
    "language": "$LANG",
    "compiled": $COMPILED,
    "compiler_exec": "$COMP_EXEC",
    "compiler_flags": [
	      "$COMP_FLAG1",
        "$COMP_FLAG2"
    ],
    "exec": "$EXEC",
    "exec_flags": [
        "$EXEC_FLAG1",
        "$EXEC_FLAG2"
    ],
    "known_naming": [
        "$KNOWN_NAME1",
        "$KNOWN_NAME2"
    ],
    "file_extension": "$FILE_EXTENSION"
}
```

- $LANG: Replace this with the name of your language (in lowercase)
- $COMPILED: This is a bool value. Replace it with `true` if the language needs to be compiled, or with `false` if it doesn't.
- $COMPILER_EXEC: Replace this with the name of the package that compiles the code of your language. It can be left empty if there's no need for compiling.
- $COMPILER_FLAGS: Replace this with any flag you want to pass to the compiler. I recommend you to pass a flag that disables color output (since it will break the formatting when print by Discord) and, due to limitations of the code, the last flag must be the one that means "create the executable in the following path". It can be left empty if there's no need for compiling.
- $EXEC: Replace this with the name of the package that runs the code of your language. It can be left empty if there's no need for it (running a compiled binary)
- $EXEC_FLAG: Replace this with any flag you want to pass to the package that runs your code. It can be left empty.
- $KNOWN_NAME: Replace this with the different ways to name the programming language you want to add. There must be at least one value here.
- $FILE_EXTENSION: Replace this with the file extension used by the files of your programming language.

In order to make things simpler, I recommend to copy an already made .json file (ie: `bash.json` for non-compiled languages, or `cpp.json` for compiled languages) and modify the values there. You can use the other `.json` files as reference when making your own.

If you want the language to be added officially, make a pull request of the `.json` file.
