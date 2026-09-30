// Valida arquivos .xs com o lexer e o parser oficiais do Xano.
//
// Por que isto existe: a extensão do VS Code só valida o arquivo que está
// aberto, e o push para o Xano é irreversível — um endpoint com erro de
// sintaxe substitui um que funcionava. Validar os 45 de uma vez, antes de
// empurrar, custa dois segundos.
//
// Uso:
//   node scripts/validar_xanoscript.mjs apis/pet_bits/*.xs tables/*.xs
//
// O parser vem da extensão instalada (`xano.xanoscript`). Se a versão dela
// mudar, ajuste EXTENSAO abaixo — ou rode com a variável de ambiente:
//   XANO_EXT=/caminho/da/extensao node scripts/validar_xanoscript.mjs ...

import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const EXTENSAO =
  process.env.XANO_EXT ||
  join(homedir(), ".vscode", "extensions", "xano.xanoscript-0.5.12");

const SERVIDOR = join(EXTENSAO, "language-server");

let lexDocument, xanoscriptParser;
try {
  ({ lexDocument } = await import(
    pathToFileURL(join(SERVIDOR, "lexer", "lexer.js")).href
  ));
  ({ xanoscriptParser } = await import(
    pathToFileURL(join(SERVIDOR, "parser", "parser.js")).href
  ));
} catch (erro) {
  console.error(
    `Não achei o parser do Xano em:\n  ${SERVIDOR}\n\n` +
      "Instale a extensão `xano.xanoscript` no VS Code, ou aponte XANO_EXT\n" +
      "para a pasta dela."
  );
  process.exit(2);
}

const alvos = process.argv.slice(2);
if (alvos.length === 0) {
  console.error("uso: node scripts/validar_xanoscript.mjs <arquivo.xs> [...]");
  process.exit(2);
}

let falhas = 0;
for (const caminho of alvos) {
  const erros = [];
  try {
    const fonte = readFileSync(caminho, "utf8");
    const lex = lexDocument(fonte);
    for (const e of lex.errors ?? []) {
      erros.push(`lexer linha ${e.line}: ${e.message}`);
    }
    // scheme null: o parser deduz pelo conteúdo se é query, function ou table.
    const parser = xanoscriptParser(fonte, null, lex);
    for (const e of parser.errors ?? []) {
      erros.push(`parser linha ${e.token?.startLine ?? "?"}: ${e.message}`);
    }
  } catch (erro) {
    erros.push(`exceção: ${erro.message}`);
  }

  if (erros.length === 0) {
    console.log(`ok     ${caminho}`);
    continue;
  }
  falhas++;
  console.log(`FALHA  ${caminho}`);
  for (const e of erros.slice(0, 5)) console.log(`       ${e}`);
}

console.log(
  falhas === 0
    ? `\n${alvos.length} arquivo(s), todos válidos`
    : `\n${falhas} de ${alvos.length} arquivo(s) com erro`
);
process.exit(falhas === 0 ? 0 : 1);
