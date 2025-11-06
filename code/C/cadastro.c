#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>

#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

int is_valid_name(const char *name);
int is_valid_email_format(const char *email, const char *role);

int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "ERRO: Numero incorreto de argumentos. Esperado: <role> <nome> <email> <senha>\n");
        return 1;
    }
    setlocale(LC_ALL, "Portuguese");
    char *role_final = argv[1];
    char *nome_original = argv[2];
    char *email = argv[3];
    char *senha = argv[4];
    char nome_formatado[MAX_STR_LEN];
    strcpy(nome_formatado, nome_original);
    if (!is_valid_name(nome_formatado)) {
        fprintf(stderr, "ERRO_VALIDACAO: Nome invalido. Use apenas letras e espacos.\n");
        return 2;
    }
    if (strlen(nome_formatado) > 0) {
        nome_formatado[0] = toupper(nome_formatado[0]);
    }
    if (!is_valid_email_format(email, role_final)) {
        if (strcmp(role_final, "USER") == 0) {
            fprintf(stderr, "ERRO_VALIDACAO: Email invalido. Alunos devem usar: @aluno.sge.com.br\n");
        } else {
            fprintf(stderr, "ERRO_VALIDACAO: Email invalido. Professores devem usar: @professor.sge.com.br\n");
        }
        return 3;
    }
    if (strlen(senha) < 4) {
        fprintf(stderr, "ERRO_VALIDACAO: Senha deve ter no minimo 4 caracteres.\n");
        return 4;
    }
    FILE *fp = fopen(TEMP_FILE, "w");
    if (fp == NULL) {
        fprintf(stderr, "ERRO: Erro ao abrir arquivo temporario para escrita!\n");
        return 5;
    }
    fprintf(fp, "{\n");
    fprintf(fp, "    \"nome\": \"%s\",\n", nome_formatado);
    fprintf(fp, "    \"email\": \"%s\",\n", email);
    fprintf(fp, "    \"role\": \"%s\",\n", role_final);
    fprintf(fp, "    \"senha_simples\": \"%s\"\n", senha);
    fprintf(fp, "}\n");
    fclose(fp);
    return 0;
}

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

int is_valid_email_format(const char *email, const char *role) {
    const char *suffix_aluno = "@aluno.sge.com.br";
    const char *suffix_professor = "@professor.sge.com.br";
    size_t len_email = strlen(email);
    if (strcmp(role, "USER") == 0) {
        size_t len_suffix = strlen(suffix_aluno);
        if (len_email <= len_suffix) {
            return 0;
        }
        if (strcmp(email + len_email - len_suffix, suffix_aluno) != 0) {
            return 0;
        }
    } else if (strcmp(role, "INSTRUCTOR") == 0) {
        size_t len_suffix = strlen(suffix_professor);
        if (len_email <= len_suffix) {
            return 0;
        }
        if (strcmp(email + len_email - len_suffix, suffix_professor) != 0) {
            return 0;
        }
    } else {
        return 0;
    }
    return 1;
}
