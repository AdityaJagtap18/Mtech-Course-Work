#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc , char *argv[])
{
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char buffer[256];
    socklen_t addrlen = sizeof(serv_addr);

    if(argc < 3){
        fprintf(stderr, "usage %s hostname port\n", argv[0]);
        exit(0);    
    }

    portno = atoi(argv[2]);
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);   // UDP socket
    if (sockfd < 0)
        error("ERROR opening socket");

    server = gethostbyname(argv[1]);
    if(server == NULL)
    {
        fprintf(stderr , "ERROR, no such host\n");
        exit(0);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);

    while(1){
        bzero(buffer, 256);
        printf("You: ");
        fgets(buffer , 256 , stdin);

        // send message to server
        n = sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *)&serv_addr, addrlen);
        if(n < 0)
            error("Error on sendto");

        bzero(buffer , 256);

        // receive reply from server
        n = recvfrom(sockfd, buffer, 256, 0, NULL, NULL);
        if(n < 0)
            error("Error on recvfrom");

        printf("Server: %s", buffer);

        int i = strncmp("Bye", buffer , 3);
        if(i == 0)
            break;
    }

    close(sockfd);
    return 0;
}

