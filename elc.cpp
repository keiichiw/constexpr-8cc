#include "elc.hpp"

int main() {
  // Compile-time
  constexpr buffer buf = elc(); // Convert ELVM IR to target language
  constexpr unsigned int output_size = buf.size;

  static_assert(0 <= output_size && output_size < ELC_OUTPUT_LIMIT, "elc: Error");

  // Run-time
  for(int i = 0; i < output_size; ++i) {
    putchar(buf.b[i]);
  }
}
