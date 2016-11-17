#include "8cc.hpp"

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
