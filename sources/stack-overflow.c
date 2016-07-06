// Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>


# ifndef CPP
# include <stdlib.h> // EXIT_SUCCESS
# include <stdio.h> // fopen, fread, fclose, fprintf, stderr.
# endif // CPP


void
read_file(FILE *stream)
{
    char buffer[50];
    fread(buffer, 1, 1024, stream);
    return;
}


int
main(int argc, char **argv)
{
    if (argc == 2) {
        FILE *stream = fopen(argv[1], "rb");
        if (stream == NULL) {
            fprintf(stderr, "Failed to open the file: %s\n", argv[1]);
            return EXIT_FAILURE;
        } else {
            read_file(stream);
            fclose(stream);
        }
    } else {
        fprintf(stderr, "%s\n", "One argument required!");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
