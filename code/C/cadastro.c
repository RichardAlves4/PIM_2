#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>
#include <wctype.h>

#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

int is_valid_name(const char *name);
int is_valid_email_format(const char *email);

int main() {

    setlocale(LC_ALL, "Portuguese");

    char nome[MAX_STR_LEN], email[MAX_STR_LEN], role_input[3], role_final[15];
    char senha1[MAX_STR_LEN], senha2[MAX_STR_LEN];
    int idade = 0;
    int success = 0;

    printf("\nMÓDULO DE CADASTRO EXTERNO (C) \n");

    while (1) {
        printf("\nVocê é um estudante ou professor?\nDigite:\n\"E\" para estudante\n\"P\" para professor\n> ");

        if (scanf("%2s", role_input) != 1) {
            int c; while ((c = getchar()) != '\n' && c != EOF);
            printf("\nEntrada inválida. Tente novamente.\n");
            continue;
        }

        int c; while ((c = getchar()) != '\n' && c != EOF);

        if (role_input[0] == 'E' || role_input[0] == 'e') {
            strcpy(role_final, "USER");
            break;
        } else if (role_input[0] == 'P' || role_input[0] == 'p') {
            strcpy(role_final, "INSTRUCTOR");
            break;
        } else {
            printf("Opção inválida. Tente novamente.\n");
        }
    }

    while (1) {
        printf("Informe seu nome: ");
        if (fgets(nome, MAX_STR_LEN, stdin) == NULL) {
             printf("Erro na leitura.\n");
             continue;
        }

        size_t len = strlen(nome);
        if (len > 0 && nome[len-1] == '\n') {
            nome[len-1] = '\0';
        }

        if (is_valid_name(nome)) {
            if (strlen(nome) > 0) {
                nome[0] = toupper(nome[0]);
            }
            break;
        } else {
            printf("Nome Inválido. Use apenas letras e espaços.\n");
        }
    }

    while (1) {
        printf("Informe seu melhor email: ");
        scanf("%s", email);

        if (is_valid_email_format(email)) {
            break;
        } else {
            printf("Email inválido. Use @gmail.com\n");
        }
    }

    while (1) {
        printf("Informe sua idade: ");
        if (scanf("%d", &idade) != 1) {
            int c; while ((c = getchar()) != '\n' && c != EOF);
            printf("Entrada inválida. Use apenas números.\n");
            continue;
        }

        if (idade < 7) {
            printf("\nIdade mínima: 7 anos\n");
            continue;
        } else if (idade > 100) {
            printf("\nIdade inválida! Tente novamente.\n");
            continue;
        } else {
            break;
        }
    }

    while (1) {
        printf("Informe uma senha forte: ");
        scanf("%s", senha1);
        printf("Repita a senha: ");
        scanf("%s", senha2);

        if (strcmp(senha1, senha2) == 0) {
            break;
        } else {
            printf("As senhas são diferentes. Tente novamente\n");
        }
    }

    // --- Geração do JSON em C ---
    FILE *fp = fopen(TEMP_FILE, "w");
    if (fp == NULL) {
        fprintf(stderr, "Erro ao abrir arquivo temporário para escrita!\n");
        return 1;
    }

    // Escreve a estrutura JSON
    fprintf(fp, "{\n");
    fprintf(fp, "    \"nome\": \"%s\",\n", nome);
    fprintf(fp, "    \"email\": \"%s\",\n", email);
    fprintf(fp, "    \"idade\": %d,\n", idade);
    fprintf(fp, "    \"role\": \"%s\",\n", role_final);
    fprintf(fp, "    \"senha_simples\": \"%s\"\n", senha1);
    fprintf(fp, "}\n");

    fclose(fp);

    printf("\nCADASTRO CONCLUÍDO\n");

    return 0;
}

// --- Implementação das Funções de Validação ---

// Simula a validação RF03 (apenas letras e espaços)
int is_valid_name(const char *name) {
    if (name == NULL || *name == '\0') {
        return 0;
    }

    int has_letter = 0;

    for (size_t i = 0; i < strlen(name); i++) {
            char c = name[i];

            if (!isalpha(c) && !isspace(c)) {
                return 0;
        }
        if (isalpha(c)) {
            has_letter = 1;
        }
    }
    return has_letter;
}

// Simula a validação RF03 - Verifica se o e-mail termina com "@gmail.com"
int is_valid_email_format(const char *email) {
    const char *suffix = "@gmail.com";
    size_t len_email = strlen(email);
    size_t len_suffix = strlen(suffix);

    if (len_email <= len_suffix) {
        return 0;
    }

    if (strcmp(email + len_email - len_suffix, suffix) != 0) {
        return 0;
    }
        return 1;
}
