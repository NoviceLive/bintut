// Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>


# ifndef CPP
# include <stdlib.h> // EXIT_SUCCESS, malloc, free.
# endif // CPP


int
main(void)
{
    char *buffer = malloc(50);

    free(buffer);
    free(buffer);

    return EXIT_SUCCESS;
}
