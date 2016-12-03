# constexpr-8cc: Compile-time C Compiler [![Build Status](https://travis-ci.org/kw-udon/constexpr-8cc.svg?branch=master)](https://travis-ci.org/kw-udon/constexpr-8cc)

[constexpr-8cc](https://github.com/kw-udon/constexpr-8cc) is a compile-time C compiler implemented as C++14 constant expressions.
This enables you to **compile while you compile!**
This project is a port of [8cc](https://github.com/rui314/8cc) built on [ELVM Infrastructure](https://github.com/shinh/elvm).

[Constant expressions in C++](http://en.cppreference.com/w/cpp/language/constant_expression) are expressions that can be evaluated at compile-time.
In C++14, [by relaxing constrains](https://isocpp.org/files/papers/N3652.html), constant expressions became so **powerful** that **a C compiler can be implemented in**!

In constexpr-8cc, the main routine for compilations of C programs is implemented in a C++14 `constexpr` function.
Therefore, if you compile `8cc.cpp` to a binary file by g++, compilation of a C program will be performed as a compile-time computation and the result of this C compilation will be embedded into the generated binary.
In this sense, constexpr-8cc is a **compile-time C compiler**.

The following is the `main` function in [8cc.cpp](https://github.com/kw-udon/constexpr-8cc/blob/master/8cc.cpp).
```c++
int main() {
  // Compile-time
  constexpr buffer buf = eight_cc(); // Compile C code into ELVM IR
  constexpr unsigned int output_size = buf.size;

  static_assert(0 <= output_size && output_size < EIGHT_CC_OUTPUT_LIMIT, "8cc: Error");

  // Run-time
  for(int i = 0; i < output_size; ++i) {
    putchar(buf.b[i]);
  }
}
```
In this program, the return value of `eight_cc` is stored into the variable `buf` with a `constexpr` specifier.
Thus, you will find that the compilation of a C program is done in compile-time.

## Usage

`constexpr-8cc` works on Linux and OS X and requires [**g++ 6.2**](https://gcc.gnu.org/gcc-6/).
(The version of g++ is **important!**)

### Compilation by `run_8cc.py`
In order to try constexpr-8cc easily, use `run_8cc.py`.
```shell
$ ./run_8cc.py x86 ./test/hello.c -o ./hello.exe # It takes about 3 minutes on my laptop
$ chmod +x ./hello.exe                           # 'hello.exe' is i386-linux binary
$ ./hello.exe
Hello, world!
```
You can change the target language of compilations like the following:
```shell
$ ./run_8cc.py py ./test/hello.c -o ./hello.py # target language is Python
$ python ./hello.py
Hello, world!
```
For more information about this script, type `$ ./run_8cc.py -h`.

### Compilation by hand
If you want to compile `8cc.cpp` manually, please look at `config.hpp`.
In this file, the variable `EIGHT_CC_INPUT_FILE` is defined.
`EIGHT_CC_INPUT_FILE` should be a name of a file that contains a source C program as a C++ string literal.
This string will be embedded in 8cc.cpp at pre-processing-time and used as an input of the compile-time computation.

So, before compiling `8cc.cpp` manually, you have to convert a raw program to a string literal like the following:
```shell
$ sed '1s/^/R"(/' ./test/hello.c | sed '$s/$/\n)"/' > ./test/hello.c.txt # Convert C to string literal
$ g++-6 ./8cc.cpp -o eir_gen.out
$ ./eir_gen.out > ./test/hello.eir       # eir_gen.out outputs ELVM IR
$ sed -i '1s/^/R"(x86/' ./test/hello.eir # Convert IR to string literal
$ sed -i '$s/$/\n)"/' ./test/hello.eir
$ g++-6 ./elc.cpp -o exe_gen.out
$ ./exe_gen.out > ./hello.exe            # exe_gen.out outputs i386-linux binary
$ chmod +x ./hello.exe
$ ./hello.exe
Hello, world!
```
## How was constexpr-8cc generated?
When you see [`8cc.hpp`](https://github.com/kw-udon/constexpr-8cc/blob/master/8cc.hpp), you will know this program was not written by hand.
Actually, I used [ELVM Compiler Infrastructure](https://github.com/shinh/elvm) to generate it.
I just implemented a translator from ELVM IR to C++14 constexpr [here](https://github.com/shinh/elvm/pull/15).

## Author
**Keiichi Watanabe** (udon.watanabe [at] gmail.com)

## References
* [8cc](https://github.com/rui314/8cc) ([@rui314](https://github.com/rui314))
  - A very cool C compiler. constexpr-8cc is a C++14's constexpr port of 8cc.
* [ELVM](https://github.com/shinh/elvm) ([@shinh](https://github.com/shinh))
  - ELVM(EsoLang Virtual Machine) is a parody project of LLVM, but dedicated to Esoteric Languages. constexpr-8cc is built on ELVM infrastructure.
* [8cc.vim](https://github.com/rhysd/8cc.vim) ([@rhysd](https://github.com/rhysd)), [8cc.tex](https://github.com/hak7a3/8cc.tex) ([@hak7a3](https://github.com/hak7a3))
  - constexpr-8cc is influenced by these projects.
* [Compile-time Brainf\*ck compiler](https://github.com/bolero-MURAKAMI/Sprout/blob/master/example/brainfuck/x86_compile.cpp) ([@bolero-MURAKAMI](https://github.com/bolero-MURAKAMI))
  - I got some ideas from this program.
  
* [My blog post (in Japanese)](http://kw-udon.hatenablog.com/entry/2016/12/03/201722)
