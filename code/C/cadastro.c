#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Definindo o nome do arquivo tempor�rio que o Python ler�
#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

// --- Prot�tipos das Fun��es de Valida��o ---
int is_valid_name(const char *name);
int is_valid_email_format(const char *email);

int main() {
    // Vari�veis para armazenar os dados coletados
    char nome[MAX_STR_LEN], email[MAX_STR_LEN], role_input[3], role_final[15];
    char senha1[MAX_STR_LEN], senha2[MAX_STR_LEN];
    int idade = 0;
    int success = 0;

    printf("\n==================================\n");
    printf("     M�DULO DE CADASTRO EXTERNO (C) \n");
    printf("==================================\n");

    // 1. Loop para coletar a ROLE (E/P)
    while (1) {
        printf("\nVoc� � um estudante ou professor?\nDigite:\n\"E\" para estudante\n\"P\" para professor\n> ");
        if (scanf("%2s", role_input) != 1) { // Leitura segura de no m�ximo 2 caracteres
            // Limpa o buffer em caso de entrada inv�lida (ex: letras n�o ASCII)
            int c; while ((c = getchar()) != '\n' && c != EOF);
            printf("\nEntrada inv�lida. Tente novamente.\n");
            continue;
        }

        // Converte para mai�sculas
        if (role_input[0] == 'E' || role_input[0] == 'e') {
            strcpy(role_final, "USER");
            break;
        } else if (role_input[0] == 'P' || role_input[0] == 'p') {
            strcpy(role_final, "INSTRUCTOR");
            break;
        } else {
            printf("Op��o inv�lida. Tente novamente.\n");
        }
    }

    // 2. Loop para coletar o NOME (e validar is_valid_name)
    while (1) {
        printf("Informe seu nome: ");
        // Leitura de uma linha inteira (fgets) para nomes compostos
        if (fgets(nome, MAX_STR_LEN, stdin) == NULL) {
             printf("Erro na leitura.\n");
             continue;
        }
        // Limpar o newline e espa�os
        size_t len = strlen(nome);
        if (len > 0 && nome[len-1] == '\n') {
            nome[len-1] = '\0';
        }

        if (is_valid_name(nome)) {
            // Se o nome for v�lido, capitalizamos a primeira letra (opcional, mas bom)
            if (strlen(nome) > 0) {
                nome[0] = toupper(nome[0]);
            }
            break;
        } else {
            printf("Nome Inv�lido. Use apenas letras e espa�os.\n");
        }
    }

    // 3. Loop para coletar o EMAIL (e validar @gmail.com)
    while (1) {
        printf("Informe seu melhor email: ");
        scanf("%s", email); // Leitura mais simples, sem espa�os

        if (is_valid_email_format(email)) {
            // Em Python, voc� faria a checagem no banco de dados.
            // Aqui, apenas validamos o formato.
            break;
        } else {
            printf("Email inv�lido. Use @gmail.com\n");
        }
    }

    // 4. Loop para coletar a IDADE (e validar 7-100)
    while (1) {
        printf("Informe sua idade: ");
        if (scanf("%d", &idade) != 1) {
            // Limpa o buffer em caso de entrada n�o num�rica
            int c; while ((c = getchar()) != '\n' && c != EOF);
            printf("Entrada inv�lida. Use apenas n�meros.\n");
            continue;
        }

        if (idade < 7) {
            printf("\nIdade m�nima: 7 anos\n");
            continue;
        } else if (idade > 100) {
            printf("\nIdade inv�lida! Tente novamente.\n");
            continue;
        } else {
            break;
        }
    }

    // 5. Loop para coletar e comparar as SENHAS (senha1 == senha2)
    while (1) {
        printf("Informe uma senha forte: ");
        scanf("%s", senha1);
        printf("Repita a senha: ");
        scanf("%s", senha2);

        if (strcmp(senha1, senha2) == 0) { // Compara strings
            break;
        } else {
            printf("As senhas s�o diferentes. Tente novamente\n");
        }
    }

    // --- Gera��o do JSON em C ---
    FILE *fp = fopen(TEMP_FILE, "w");
    if (fp == NULL) {
        fprintf(stderr, "Erro ao abrir arquivo tempor�rio para escrita!\n");
        return 1; // Retorna c�digo de erro
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

    printf("\nCADASTRO CONCLU�DO EM C. Dados salvos para processamento em Python.\n");

    return 0; // Sucesso
}

// --- Implementa��o das Fun��es de Valida��o ---

// Simula a valida��o RF03 (apenas letras e espa�os)
int is_valid_name(const char *name) {
    if (name == NULL || *name == '\0') {
        return 0; // Nome vazio
    }
    for (size_t i = 0; i < strlen(name); i++) {
        // Verifica se o caractere n�o � uma letra (incluindo acentuadas, o que C nativo n�o faz bem) ou espa�o
        // Para acentuadas, voc� teria que usar uma biblioteca de i18n ou l�gica complexa.
        // Aqui, apenas verificamos A-Z, a-z e espa�o.
        if (!isalpha(name[i]) && !isspace(name[i])) {
            return 0; // Falha na valida��o
        }
    }
    return 1; // Sucesso
}

// Simula a valida��o RF03 - Verifica se o e-mail termina com "@gmail.com"
int is_valid_email_format(const char *email) {
    const char *suffix = "@gmail.com";
    size_t len_email = strlen(email);
    size_t len_suffix = strlen(suffix);

    if (len_email < len_suffix) {
        return 0; // Email muito curto
    }

    // Compara o final da string (len_email - len_suffix)
    if (strcmp(email + len_email - len_suffix, suffix) == 0) {
        return 1; // Sucesso
    } else {
        return 0; // Falha na valida��o
    }
}
