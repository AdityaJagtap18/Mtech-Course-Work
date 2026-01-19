// pkt_sniffer.c
// Compile: gcc -o pkt_sniffer pkt_sniffer.c
// Run: sudo ./pkt_sniffer <interface>
// Example: sudo ./pkt_sniffer lo
//
// Note: requires root. This is read-only: it receives frames and prints headers.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <net/ethernet.h>
#include <netinet/ip.h>
#include <netpacket/packet.h>
#include <net/if.h>
#include <sys/ioctl.h>

#define BUF_SIZE 65536

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <interface>\n", argv[0]);
        return 1;
    }
    const char *ifname = argv[1];

    // create raw socket to capture all ethernet protocols
    int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sock < 0) {
        perror("socket(AF_PACKET)");
        return 1;
    }

    // bind to specific interface
    struct sockaddr_ll sll;
    memset(&sll, 0, sizeof(sll));
    sll.sll_family = AF_PACKET;
    sll.sll_protocol = htons(ETH_P_ALL);
    sll.sll_ifindex = if_nametoindex(ifname);
    if (sll.sll_ifindex == 0) {
        fprintf(stderr, "Unknown interface %s\n", ifname);
        close(sock);
        return 1;
    }
    if (bind(sock, (struct sockaddr*)&sll, sizeof(sll)) < 0) {
        perror("bind");
        close(sock);
        return 1;
    }

    unsigned char buf[BUF_SIZE];
    while (1) {
        ssize_t len = recvfrom(sock, buf, sizeof(buf), 0, NULL, NULL);
        if (len < 0) {
            if (errno == EINTR) continue;
            perror("recvfrom");
            break;
        }
        if (len < (ssize_t)sizeof(struct ethhdr)) continue;
        struct ethhdr *eth = (struct ethhdr*)buf;

        printf("Frame: len=%zd  Ethertype=0x%04x\n", len, ntohs(eth->h_proto));

        // if IP packet, parse IP header
        if (ntohs(eth->h_proto) == ETH_P_IP && len >= (ssize_t)(sizeof(struct ethhdr) + sizeof(struct ip))) {
            struct ip *ip = (struct ip*)(buf + sizeof(struct ethhdr));
            char src[INET_ADDRSTRLEN], dst[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &ip->ip_src, src, sizeof(src));
            inet_ntop(AF_INET, &ip->ip_dst, dst, sizeof(dst));
            printf("  IP  %s -> %s  proto=%u ttl=%u\n", src, dst, ip->ip_p, ip->ip_ttl);
        }
    }

    close(sock);
    return 0;
}
