#include <winsock2.h>
#include <windows.h>
#include <stdio.h>

#pragma comment(lib, "ws2_32.lib")

SOCKET clientSocket;
HANDLE hThread;

DWORD WINAPI ClientThread(LPVOID lpParam) {
    char buffer[512];
    int bytesReceived;

    while ((bytesReceived = recv(clientSocket, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[bytesReceived] = '\0';
        printf("Server: %s\n", buffer);
    }

    printf("Disconnected from server.\n");
    return 0;
}

int main() {
    WSADATA wsa;
    struct sockaddr_in server;
    char *server_ip = "127.0.0.1";
    int port = 12345;

    printf("Starting client...\n");

    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) {
        printf("WSAStartup failed. Error: %d\n", WSAGetLastError());
        return 1;
    }

    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == INVALID_SOCKET) {
        printf("Could not create socket: %d\n", WSAGetLastError());
        return 1;
    }

    server.sin_addr.s_addr = inet_addr(server_ip);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    if (connect(clientSocket, (struct sockaddr *)&server, sizeof(server)) < 0) {
        printf("Connection failed: %d\n", WSAGetLastError());
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    printf("Connected to server %s:%d\n", server_ip, port);

    // Create thread to listen for server messages
    hThread = CreateThread(NULL, 0, ClientThread, NULL, 0, NULL);
    if (hThread == NULL) {
        printf("Failed to create thread.\n");
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    // Main thread: send messages from user input
    char msg[256];
    while (1) {
        fgets(msg, sizeof(msg), stdin);
        if (strncmp(msg, "exit", 4) == 0) break;
        send(clientSocket, msg, strlen(msg), 0);
    }

    closesocket(clientSocket);
    WSACleanup();
    return 0;
}
