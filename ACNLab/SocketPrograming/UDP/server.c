#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Port No not provided. Program terminated\n");
        exit(1);
    }

    int sockfd, portno, n;
    char buffer[255];

    struct sockaddr_in serv_addr, cli_addr;
    socklen_t clilen;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0); // UDP socket
    if (sockfd < 0)
    {
        error("Error opening socket.");
    }

    bzero((char *)&serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);

    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        error("Binding Failed.");

    clilen = sizeof(cli_addr);

    while (1)
    {
        bzero(buffer, 255);

        // receive message from client
        n = recvfrom(sockfd, buffer, 255, 0, (struct sockaddr *)&cli_addr, &clilen);
        if (n < 0)
            error("Error on recvfrom");
        printf("Client : %s\n", buffer);

        bzero(buffer, 255);
        fgets(buffer, 255, stdin);

        // send reply to client
        n = sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *)&cli_addr, clilen);
        if (n < 0)
            error("Error on sendto");

        int i = strncmp("Bye", buffer, 3);
        if (i == 0)
            break;
    }

    close(sockfd);
    return 0;
}

