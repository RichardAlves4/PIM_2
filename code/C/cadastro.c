#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>

#define TEMP_FILE "temp_cadastro.json"
#define MAX_STR_LEN 100

// Verifica se o nome contém apenas letras e espaços.
int is_valid_name(const char *name);
// Verifica se o email segue o formato de sufixo esperado para a 'role' (papel/função).
int is_valid_email_format(const char *email, const char *role);

int main(int argc, char *argv[]) {
    // 1. Verificação do número de argumentos
    if (argc != 5) {
        // argc conta o nome do programa + 4 argumentos esperados, totalizando 5.
        fprintf(stderr, "ERRO: Numero incorreto de argumentos. Esperado: <role> <nome> <email> <senha>\n");
        return 1; // Retorna 1 (código de erro)
    }
    // Configura a localidade para o idioma Português
    setlocale(LC_ALL, "Portuguese");
    // 2. Mapeamento dos Argumentos da Linha de Comando 
    char *role_final = argv[1]; // Exemplo: "USER" ou "INSTRUCTOR"
    char *nome_original = argv[2]; // Nome passado como argumento
    char *email = argv[3]; // Email passado como argumento
    char *senha = argv[4]; // Senha passada como argumento
    char nome_formatado[MAX_STR_LEN];
    // Cria uma cópia do nome para que possamos modificá-lo
    strcpy(nome_formatado, nome_original);

    // 3. Validação do Nome
    if (!is_valid_name(nome_formatado)) {
        fprintf(stderr, "ERRO_VALIDACAO: Nome invalido. Use apenas letras e espacos.\n");
        return 2; // Retorna 2 (código de erro de validação de nome)
    }

    // 4. Formatação do Nome (Capitalização da Primeira Letra)
    if (strlen(nome_formatado) > 0) {
        // Converte o primeiro caractere para maiúsculo.
        nome_formatado[0] = toupper(nome_formatado[0]);
    }

    // 5. Validação do Formato do E-mail (Baseado na Role)
    if (!is_valid_email_format(email, role_final)) {
        // Mensagem de erro específica dependendo da role
        if (strcmp(role_final, "USER") == 0) {
            fprintf(stderr, "ERRO_VALIDACAO: Email invalido. Alunos devem usar: @aluno.sge.com.br\n");
        } else { // Presume-se INSTRUCTOR se não for USER e tiver passado pela função.
            fprintf(stderr, "ERRO_VALIDACAO: Email invalido. Professores devem usar: @professor.sge.com.br\n");
        }
        return 3; // Retorna 3 (código de erro de validação de email)
    }

    // 6. Validação da Senha (Comprimento Mínimo)
    if (strlen(senha) < 4) {
        fprintf(stderr, "ERRO_VALIDACAO: Senha deve ter no minimo 4 caracteres.\n");
        return 4; // Retorna 4 (código de erro de validação de senha)
    }

    // 7. Abertura do Arquivo Temporário para Escrita
    // "w" (write) abre o arquivo para escrita; se ele existir, seu conteúdo é apagado.
    FILE *fp = fopen(TEMP_FILE, "w");

    if (fp == NULL) {
        fprintf(stderr, "ERRO: Erro ao abrir arquivo temporario para escrita!\n");
        return 5; // Retorna 5 (código de erro de E/S de arquivo)
    }

    // 8. Escrita dos Dados no Formato JSON no Arquivo
    fprintf(fp, "{\n");
    fprintf(fp, "    \"nome\": \"%s\",\n", nome_formatado);
    fprintf(fp, "    \"email\": \"%s\",\n", email);
    fprintf(fp, "    \"role\": \"%s\",\n", role_final);
    fprintf(fp, "    \"senha_simples\": \"%s\"\n", senha);
    fprintf(fp, "}\n");
    // 9. Fechamento do Arquivo e Saída
    fclose(fp); // Libera o recurso de arquivo.
    return 0; // Retorna 0 (sucesso)
}

int is_valid_name(const char *name) {
    // 1. Verificação de Nulidade/Vazio
    if (name == NULL || *name == '\0') {
        return 0; // Nome nulo ou vazio é inválido.
    }

    int has_letter = 0; // Flag para garantir que o nome não seja apenas espaços

    // 2. Iteração e Validação de Caracteres
    for (size_t i = 0; i < strlen(name); i++) {
        char c = name[i];
        // Verifica se o caractere NÃO é uma letra E NÃO é um espaço.
        if (!isalpha(c) && !isspace(c)) {
            return 0; // Caractere inválido encontrado.
        }
        // Se for uma letra, ativa a flag
        if (isalpha(c)) {
            has_letter = 1;
        }
    }
    // Retorna a flag 'has_letter', garantindo que haja pelo menos uma letra no nome.
    return has_letter;
}

int is_valid_email_format(const char *email, const char *role) {
    const char *suffix_aluno = "@aluno.sge.com.br";
    const char *suffix_professor = "@professor.sge.com.br";
    size_t len_email = strlen(email);

    // 1. Lógica para "USER" (Aluno)
    if (strcmp(role, "USER") == 0) {
        size_t len_suffix = strlen(suffix_aluno);
        // O email deve ser maior que o sufixo
        if (len_email <= len_suffix) {
            return 0;
        }
        // Compara a parte final (o sufixo) do email com o sufixo esperado.
        if (strcmp(email + len_email - len_suffix, suffix_aluno) != 0) {
            return 0;
        }
        // 2. Lógica para "INSTRUCTOR" (Professor)
    } else if (strcmp(role, "INSTRUCTOR") == 0) {
        size_t len_suffix = strlen(suffix_professor);
        // O email deve ser maior que o sufixo.
        if (len_email <= len_suffix) {
            return 0;
        }
        // Compara a parte final (o sufixo) do email com o sufixo esperado.
        if (strcmp(email + len_email - len_suffix, suffix_professor) != 0) {
            return 0;
        }
        // 3. Lógica para Role Desconhecida
    } else {
        return 0; // Role inválida ou desconhecida
    }
    // Se passou pela lógica de validação correta para sua role
    return 1;
}