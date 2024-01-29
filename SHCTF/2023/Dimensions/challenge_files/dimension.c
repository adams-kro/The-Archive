#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MEMORY_SIZE 256
#define REGISTER_SIZE 8

// VM memory
char VM_MEMORY[MEMORY_SIZE];

// VM Instructions
enum {
    LOAD_ADDR_R1, LOAD_ADDR_R2, XOR_R1R2, ADD_R1R2, STORE_R3, STORE_R4, LOAD_R2R3, LOAD_R2R4, CMP_R1R2, PRINT_CORRECT, END
};
// Memory addresses
enum {
    ADDR_STRING1 = 0x10, ADDR_STRING2 = 0x40, ADDR_USER_INPUT = 0x60, ADDR_BYTECODE = 0x70
};

char obfuscated_string1[] = {0xa9, 0x6e, 0x1e, 0x75, 0x15, 0x11, 0x5f, 0x65, 0x41, 0x42, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41};
char obfuscated_string2[] = {0xfa, 0x26, 0x5d, 0x21, 0x53, 0x6a, 0x68, 0x17, 0x48, 0x19, 0x02, 0x1e, 0x4f, 0x09, 0x7e, 0x3c};  // Extend the encoded bytes

int main() {
    printf("                                                 \n");
    printf("                     [+]                         \n");
    printf("                    /   \\                        \n");
    printf("                   /_____\\                       \n");
    printf("                  /       \\                      \n");
    printf("                 /   [_]   \\                     \n");
    printf("                [_______]                        \n");
    printf("                                                 \n");
    printf("               [Veiled Dimensions]               \n\n");


    // Decode and load strings
    for (size_t i = 0; i < sizeof(obfuscated_string1); i++) {
        VM_MEMORY[ADDR_STRING1 + i] = obfuscated_string1[i] ^ 0x54;
        VM_MEMORY[ADDR_STRING2 + i] = obfuscated_string2[i] ^ 0x54;
    }
    // null terminate the strings
    VM_MEMORY[ADDR_STRING1 + sizeof(obfuscated_string1)] = '\0';
    VM_MEMORY[ADDR_STRING2 + sizeof(obfuscated_string2)] = '\0';

    unsigned char bytecode[] = {
        LOAD_ADDR_R1, ADDR_STRING1, LOAD_ADDR_R2, ADDR_STRING2,
        XOR_R1R2, STORE_R3,
        LOAD_ADDR_R1, ADDR_STRING1 + 8, LOAD_ADDR_R2, ADDR_STRING2 + 8,
        ADD_R1R2, STORE_R4,
        LOAD_ADDR_R1, ADDR_USER_INPUT, LOAD_R2R3, CMP_R1R2,
        LOAD_ADDR_R1, ADDR_USER_INPUT + 8, LOAD_R2R4, CMP_R1R2,
        PRINT_CORRECT,
        END
    };

    char user_input[18];
    printf("Enter the key: ");
    fgets(user_input, sizeof(user_input), stdin);
    user_input[strcspn(user_input, "\n")] = '\0';

    // Load bytecode
    unsigned char *bytecode_ptr = VM_MEMORY + ADDR_BYTECODE;
    unsigned char *current_bytecode = bytecode;
    while (*current_bytecode != END) {
        *bytecode_ptr++ = *current_bytecode++;
    }

    // Load user input
    strncpy((char*)(VM_MEMORY + ADDR_USER_INPUT), user_input, REGISTER_SIZE * 2);

    // Implementation for the VM
    unsigned char *ip = VM_MEMORY + ADDR_BYTECODE;  // instruction pointer

    char *R1 = NULL;
    char *R2 = NULL;
    char R3[REGISTER_SIZE] = {0};
    char R4[REGISTER_SIZE] = {0};

    while (*ip != END) {
        printf("%x ", *ip);
        switch (*ip) {
            case LOAD_ADDR_R1:
                R1 = (char*) (VM_MEMORY + *(++ip));
                break;

            case LOAD_ADDR_R2:
                R2 = (char*) (VM_MEMORY + *(++ip));
                break;

            case LOAD_R2R3:
                R2 = R3;
                break;
            
            case LOAD_R2R4:
                R2 = R4;
                break;
            
            case STORE_R3: 
                for (int i = 0; i < REGISTER_SIZE; i++) {
                    *(R3 + i) = *(R1 + i);
                }      
                break;
            
            case STORE_R4:
                for (int i = 0; i < REGISTER_SIZE; i++) {
                    *(R4 + i) = *(R1 + i);
                }

            case XOR_R1R2:
                for (int i = 0; i < REGISTER_SIZE; i++) {
                    R1[i] ^= R2[i];
                }
                break;

            case ADD_R1R2:
                for (int i = 0; i < REGISTER_SIZE; i++) {
                    R1[i] += R2[i];
                }
                break;

            case CMP_R1R2:
                for (int i = 0; i < REGISTER_SIZE; i++) {
                    if (*(R1 + i) != *(R2 + i)) {
                        printf("Incorrect key!\n");
                        exit(1);
                    }
                }

            case PRINT_CORRECT:
                printf("Correct key!\n");
                exit(0);

            default:
                printf("Invalid instruction: %x\n", *ip);
                exit(1);
        }

        ip++;  // Move to the next instruction
    }
    return 0;
}
