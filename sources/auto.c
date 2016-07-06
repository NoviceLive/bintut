// Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>


# ifndef CPP
# include <stdlib.h> // EXIT_SUCCESS.
# include <stdio.h> // fprintf, stderr.
# endif // CPP


int
main(void)
{
    auto int number;

    fprintf(stderr, "%p\n", &number);

    return EXIT_SUCCESS;
}
