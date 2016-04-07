/*
 * Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>
 */


# ifndef CPP
# include <stdlib.h>
# endif /* CPP */


int
main(int argc, char **argv)
{
  char *buffer = malloc(50);
  free(buffer);
  free(buffer);

  return EXIT_SUCCESS;
}
