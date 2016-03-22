# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# endif


int
main(void)
{
  auto int number;

  fprintf(stderr, "%p\n", &number);

  return EXIT_SUCCESS;
}
