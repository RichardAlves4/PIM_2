#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Definindo o nome do arquivo temporário que o Python lerá
#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

// --- Protótipos das Funções de Validação ---
int is_valid_name(const char *name);
int is_valid_email_format(const char *email);

int main() {
    // Variáveis para armazenar os dados coletados
    char nome[MAX_STR_LEN], email[MAX_STR_LEN], role_input[3], role_final[15];
    char senha1[MAX_STR_LEN], senha2[MAX_STR_LEN];
    int idade = 0;
    int success = 0;

    printf("\n==================================\n");
    printf("     MÓDULO DE CADASTRO EXTERNO (C) \n");
    printf("==================================\n");

    // 1. Loop para coletar a ROLE (E/P)
    while (1) {
        printf("\nVocê é um estudante ou professor?\nDigite:\n\"E\" para estudante\n\"P\" para professor\n> ");
        if (scanf("%2s", role_input) != 1) { // Leitura segura de no máximo 2 caracteres
            // Limpa o buffer em caso de entrada inválida (ex: letras não ASCII)
            int c; while ((c = getchar()) != '\n' && c != EOF);
            printf("\nEntrada inválida. Tente novamente.\n");
            continue;
        }

        // Converte para maiúsculas
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

    // 2. Loop para coletar o NOME (e validar is_valid_name)
    while (1) {
        printf("Informe seu nome: ");
        // Leitura de uma linha inteira (fgets) para nomes compostos
        if (fgets(nome, MAX_STR_LEN, stdin) == NULL) {
             printf("Erro na leitura.\n");
             continue;
        }
        // Limpar o newline e espaços
        size_t len = strlen(nome);
        if (len > 0 && nome[len-1] == '\n') {
            nome[len-1] = '\0';
        }

        if (is_valid_name(nome)) {
            // Se o nome for válido, capitalizamos a primeira letra (opcional, mas bom)
            if (strlen(nome) > 0) {
                nome[0] = toupper(nome[0]);
            }
            break;
        } else {
            printf("Nome Inválido. Use apenas letras e espaços.\n");
        }
    }

    // 3. Loop para coletar o EMAIL (e validar @gmail.com)
    while (1) {
        printf("Informe seu melhor email: ");
        scanf("%s", email); // Leitura mais simples, sem espaços

        if (is_valid_email_format(email)) {
            // Em Python, você faria a checagem no banco de dados.
            // Aqui, apenas validamos o formato.
            break;
        } else {
            printf("Email inválido. Use @gmail.com\n");
        }
    }

    // 4. Loop para coletar a IDADE (e validar 7-100)
    while (1) {
        printf("Informe sua idade: ");
        if (scanf("%d", &idade) != 1) {
            // Limpa o buffer em caso de entrada não numérica
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

    // 5. Loop para coletar e comparar as SENHAS (senha1 == senha2)
    while (1) {
        printf("Informe uma senha forte: ");
        scanf("%s", senha1);
        printf("Repita a senha: ");
        scanf("%s", senha2);

        if (strcmp(senha1, senha2) == 0) { // Compara strings
            break;
        } else {
            printf("As senhas são diferentes. Tente novamente\n");
        }
    }

    // --- Geração do JSON em C ---
    FILE *fp = fopen(TEMP_FILE, "w");
    if (fp == NULL) {
        fprintf(stderr, "Erro ao abrir arquivo temporário para escrita!\n");
        return 1; // Retorna código de erro
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

    printf("\nCADASTRO CONCLUÍDO EM C. Dados salvos para processamento em Python.\n");

    return 0; // Sucesso
}

// --- Implementação das Funções de Validação ---

// Simula a validação RF03 (apenas letras e espaços)
int is_valid_name(const char *name) {
    if (name == NULL || *name == '\0') {
        return 0; // Nome vazio
    }
    for (size_t i = 0; i < strlen(name); i++) {
        // Verifica se o caractere não é uma letra (incluindo acentuadas, o que C nativo não faz bem) ou espaço
        // Para acentuadas, você teria que usar uma biblioteca de i18n ou lógica complexa.
        // Aqui, apenas verificamos A-Z, a-z e espaço.
        if (!isalpha(name[i]) && !isspace(name[i])) {
            return 0; // Falha na validação
        }
    }
    return 1; // Sucesso
}

// Simula a validação RF03 - Verifica se o e-mail termina com "@gmail.com"
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
        return 0; // Falha na validação
    }
}
