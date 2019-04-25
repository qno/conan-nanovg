#include <nanovg.h>

int main() {

   NVGcolor color = {11,22,33,44};
   auto transformedColor = nvgTransRGBA(color, 100);

   return 0;
}
