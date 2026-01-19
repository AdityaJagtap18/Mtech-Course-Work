// raw_echo_server.c
// Compile: gcc -o raw_echo_server raw_echo_server.c
// Run (as root): sudo ./raw_echo_server <listen_port>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <sys/socket.h>

// compute IP checksum
unsigned short csum(unsigned short *buf, int nwords) {
    unsigned long sum = 0;
    for (; nwords > 0; nwords--) sum += *buf++;
    while (sum >> 16) sum = (sum & 0xffff) + (sum >> 16);
    return (unsigned short)(~sum);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <listen_port>\n", argv[0]);
        return 1;
    }
    int listen_port = atoi(argv[1]);

    // Raw socket to receive UDP packets (kernel will include IP header)
    int rsock = socket(AF_INET, SOCK_RAW, IPPROTO_UDP);
    if (rsock < 0) { perror("socket"); return 1; }

    while (1) {
        unsigned char buf[65536];
        struct sockaddr_in src;
        socklen_t slen = sizeof(src);
        ssize_t len = recvfrom(rsock, buf, sizeof(buf), 0, (struct sockaddr*)&src, &slen);
        if (len < 0) { perror("recvfrom"); continue; }

        // Parse IP header
        struct iphdr *iph = (struct iphdr*)buf;
        int iphdr_len = iph->ihl * 4;

        // Parse UDP header
        struct udphdr *udph = (struct udphdr*)(buf + iphdr_len);
        int src_port = ntohs(udph->source);
        int dst_port = ntohs(udph->dest);
        int udp_len = ntohs(udph->len);

        if (dst_port != listen_port) {
            // not for us
            continue;
        }

        unsigned char *payload = buf + iphdr_len + sizeof(struct udphdr);
        int payload_len = udp_len - sizeof(struct udphdr);
        printf("Received %d bytes from %s:%d -> %s:%d\n",
               payload_len, inet_ntoa(*(struct in_addr*)&iph->saddr), src_port,
               inet_ntoa(*(struct in_addr*)&iph->daddr), dst_port);

        // Echo back to sender using raw socket with IP_HDRINCL
        int send_sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
        if (send_sock < 0) { perror("send_sock"); continue; }
        int one = 1;
        setsockopt(send_sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one));

        // Build IP + UDP + payload
        unsigned char packet[65536];
        memset(packet, 0, sizeof(packet));

        struct iphdr *oiph = (struct iphdr*)packet;
        struct udphdr *oudph = (struct udphdr*)(packet + sizeof(struct iphdr));
        unsigned char *opayload = packet + sizeof(struct iphdr) + sizeof(struct udphdr);

        // swap src/dst for echo
        oiph->version = 4;
        oiph->ihl = 5;
        oiph->tos = 0;
        oiph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct udphdr) + payload_len);
        oiph->id = htons(54321);
        oiph->frag_off = 0;
        oiph->ttl = 64;
        oiph->protocol = IPPROTO_UDP;
        oiph->saddr = iph->daddr; // original dst (our IP)
        oiph->daddr = iph->saddr; // original src (sender)
        oiph->check = 0;
        oiph->check = csum((unsigned short*)oiph, oiph->ihl*2);

        // UDP header: source = server port we saw as dst_port, dest = src_port
        oudph->source = htons(listen_port);
        oudph->dest   = htons(src_port);
        oudph->len    = htons(sizeof(struct udphdr) + payload_len);
        oudph->check  = 0; // leave zero (optional)

        memcpy(opayload, payload, payload_len);

        // destination sockaddr
        struct sockaddr_in dest;
        memset(&dest, 0, sizeof(dest));
        dest.sin_family = AF_INET;
        dest.sin_addr.s_addr = oiph->daddr;

        ssize_t sent = sendto(send_sock, packet, ntohs(oiph->tot_len), 0,
                              (struct sockaddr*)&dest, sizeof(dest));
        if (sent < 0) perror("sendto");
        else printf("Echoed %zd bytes back to %s:%d\n", sent - sizeof(struct iphdr) - sizeof(struct udphdr),
                    inet_ntoa(dest.sin_addr), src_port);

        close(send_sock);
    }

    close(rsock);
    return 0;
}

