// Build: gcc -O2 -Wall -o math_client math_client.c
// Run:   ./math_client 127.0.0.1 5000 "12 + 34"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUF_SIZE 1024

void die(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <server_ip> <port> <expression>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *server_ip = argv[1];
    int port = atoi(argv[2]);

    // Join remaining args into one expression string
    char expr[BUF_SIZE] = "";
    for (int i = 3; i < argc; i++) {
        strcat(expr, argv[i]);
        if (i < argc - 1) strcat(expr, " ");
    }

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) die("socket");

    struct sockaddr_in srv;
    srv.sin_family = AF_INET;
    srv.sin_port = htons(port);
    if (inet_pton(AF_INET, server_ip, &srv.sin_addr) <= 0)
        die("inet_pton");

    if (connect(sock, (struct sockaddr *)&srv, sizeof(srv)) < 0)
        die("connect");

    send(sock, expr, strlen(expr), 0);

    char buffer[BUF_SIZE];
    int n = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (n < 0) die("recv");
    buffer[n] = '\0';

    printf("Server: %s\n", buffer);

    close(sock);
    return 0;
}
