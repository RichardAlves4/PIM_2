#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>

// Definições e funções de validação omitidas para brevidade, mas devem ser mantidas
#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

int is_valid_name(const char *name);
int is_valid_email_format(const char *email);

// O executável C agora espera 5 argumentos: [1] role, [2] nome, [3] email, [4] idade, [5] senha
int main(int argc, char *argv[]) {

    // 1. Verifica se todos os argumentos foram passados (5 argumentos + nome do programa = 6)
    if (argc != 6) {
        // Envia uma mensagem de erro para a saída de erro padrão (stderr)
        fprintf(stderr, "ERRO: Numero incorreto de argumentos. Esperado: <role> <nome> <email> <idade> <senha>\n");
        return 1; // Retorna código de erro
    }

    setlocale(LC_ALL, "Portuguese");

    // 2. Extrai os dados dos argumentos
    char *role_final = argv[1];
    char *nome_original = argv[2];
    char *email = argv[3];
    int idade = atoi(argv[4]); // Converte string para inteiro
    char *senha = argv[5];

    char nome_formatado[MAX_STR_LEN];
    strcpy(nome_formatado, nome_original);

    // 3. Executa as validações do C

    // Validação de Nome
    if (!is_valid_name(nome_formatado)) {
        fprintf(stderr, "ERRO_VALIDACAO: Nome invalido. Use apenas letras e espacos.\n");
        return 2;
    }
    if (strlen(nome_formatado) > 0) {
        nome_formatado[0] = toupper(nome_formatado[0]); // Capitaliza a primeira letra
    }

    // Validação de Email
    if (!is_valid_email_format(email)) {
        fprintf(stderr, "ERRO_VALIDACAO: Email invalido. O email deve terminar com @gmail.com\n");
        return 3;
    }

    // Validação de Idade
    if (idade < 7 || idade > 100) {
        fprintf(stderr, "ERRO_VALIDACAO: Idade fora do intervalo (7-100).\n");
        return 4;
    }

    // Omitimos a verificação de senha duplicada/igual aqui, pois o Python já fará isso na interface.
    // O C apenas receberá a senha já validada.

    // 4. Geração do JSON (se chegou aqui, as validações do C passaram)
    FILE *fp = fopen(TEMP_FILE, "w");
    if (fp == NULL) {
        fprintf(stderr, "ERRO: Erro ao abrir arquivo temporario para escrita!\n");
        return 5;
    }

    // Escreve a estrutura JSON
    fprintf(fp, "{\n");
    fprintf(fp, "    \"nome\": \"%s\",\n", nome_formatado);
    fprintf(fp, "    \"email\": \"%s\",\n", email);
    fprintf(fp, "    \"idade\": %d,\n", idade);
    fprintf(fp, "    \"role\": \"%s\",\n", role_final);
    fprintf(fp, "    \"senha_simples\": \"%s\"\n", senha);
    fprintf(fp, "}\n");

    fclose(fp);

    // Sucesso
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
