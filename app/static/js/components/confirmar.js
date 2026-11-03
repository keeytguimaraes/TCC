// ============================================================
// CONFIRMAÇÃO DE AÇÕES — SIGC (componente global)
// ============================================================
// Um único modal (<dialog>) é criado pelo próprio script e serve
// a todos os módulos. Quem aciona só declara atributos no <form>:
//
//   <form action="/fornecedor/desativar/3" method="POST"
//         data-confirmar="desativar"        (desativar | reativar)
//         data-registro="fornecedor"        (tipo do registro)
//         data-nome="Ambev">                (nome exibido)
//       <button type="submit" class="btn btn-desativar">…</button>
//   </form>
//
// Opcionais: data-titulo, data-mensagem, data-explicacao,
//            data-botao (texto do botão de confirmação),
//            data-verbo ("inativar" / "ativar": troca a palavra usada no
//            título, na mensagem e no botão, sem mudar o tipo da ação).
//
// data-bloqueado (atributo presente): a ação está impedida (ex.: cliente
// com conta em aberto). O modal só informa — usa data-titulo,
// data-mensagem e data-explicacao — e NÃO oferece botão de confirmar.
// O formulário nunca é enviado nesse modo.
//
// A ação (envio do formulário) só acontece no botão de confirmar.
// Cancelar, ×, Esc e clique fora apenas fecham o modal.
// O foco inicial fica em "Cancelar". Sem JavaScript, o formulário
// continua enviando normalmente.
// ============================================================

(function () {

    "use strict";

    var TIPOS = {
        desativar: {
            titulo: function (r) { return "Desativar " + r; },
            mensagem: "Deseja desativar",
            explicacao:
                "O cadastro não será excluído. Ele deixará de aparecer " +
                "na lista principal e poderá ser reativado posteriormente.",
            botao: "Desativar",
            classe: "btn-desativar",
            icone: "fa-ban"
        },
        reativar: {
            titulo: function (r) { return "Reativar " + r; },
            mensagem: "Deseja reativar",
            explicacao:
                "O cadastro voltará a aparecer na lista principal e " +
                "poderá ser utilizado novamente no sistema.",
            botao: "Reativar",
            classe: "btn-reativar",
            icone: "fa-rotate-left"
        }
    };

    var dialogo = null;
    var ref = {};
    var pendente = null;      // { form }
    var gatilho = null;       // elemento que tinha o foco antes de abrir
    var fechando = false;

    function el(tag, classe, texto) {
        var e = document.createElement(tag);
        if (classe) e.className = classe;
        if (texto) e.textContent = texto;
        return e;
    }

    function criarDialogo() {

        dialogo = el("dialog", "confirmar");
        dialogo.setAttribute("aria-labelledby", "confirmar-titulo");
        dialogo.setAttribute("aria-describedby", "confirmar-mensagem");

        var caixa = el("div", "confirmar-caixa");

        var cab = el("div", "confirmar-cabecalho");
        ref.titulo = el("h2", "confirmar-titulo");
        ref.titulo.id = "confirmar-titulo";
        ref.fechar = el("button", "confirmar-fechar", "×");
        ref.fechar.type = "button";
        ref.fechar.setAttribute("aria-label", "Fechar");
        cab.appendChild(ref.titulo);
        cab.appendChild(ref.fechar);

        var corpo = el("div", "confirmar-corpo");
        ref.mensagem = el("p", "confirmar-mensagem");
        ref.mensagem.id = "confirmar-mensagem";
        ref.explicacao = el("p", "confirmar-explicacao");
        corpo.appendChild(ref.mensagem);
        corpo.appendChild(ref.explicacao);

        var rod = el("div", "confirmar-rodape");
        ref.cancelar = el("button", "btn btn-cancelar", "Cancelar");
        ref.cancelar.type = "button";
        ref.confirmar = el("button", "btn");
        ref.confirmar.type = "button";
        rod.appendChild(ref.cancelar);
        rod.appendChild(ref.confirmar);

        caixa.appendChild(cab);
        caixa.appendChild(corpo);
        caixa.appendChild(rod);
        dialogo.appendChild(caixa);
        document.body.appendChild(dialogo);

        ref.fechar.addEventListener("click", fechar);
        ref.cancelar.addEventListener("click", fechar);
        ref.confirmar.addEventListener("click", confirmar);

        // Clique no fundo escurecido: o alvo é o próprio <dialog>.
        dialogo.addEventListener("click", function (e) {
            if (e.target === dialogo) fechar();
        });

        // Tab / Shift+Tab circulam apenas entre ×, Cancelar e Confirmar.
        dialogo.addEventListener("keydown", function (e) {
            if (e.key !== "Tab") return;
            var itens = [ref.fechar, ref.cancelar, ref.confirmar].filter(
                function (b) { return !b.disabled && !b.hidden; }
            );
            var primeiro = itens[0];
            var ultimo = itens[itens.length - 1];
            if (e.shiftKey && document.activeElement === primeiro) {
                e.preventDefault();
                ultimo.focus();
            } else if (!e.shiftKey && document.activeElement === ultimo) {
                e.preventDefault();
                primeiro.focus();
            }
        });

        // Esc: o navegador dispara "cancel"; fechamos com animação.
        dialogo.addEventListener("cancel", function (e) {
            e.preventDefault();
            fechar();
        });

    }

    function abrir(form) {

        if (!dialogo) criarDialogo();
        if (fechando) return;

        var d = form.dataset;
        var tipo = TIPOS[d.confirmar] || TIPOS.desativar;
        var registro = d.registro || "registro";
        var nome = d.nome || "este registro";
        var bloqueado = form.hasAttribute("data-bloqueado");

        dialogo.setAttribute(
            "data-tipo",
            bloqueado ? "bloqueado" : (d.confirmar === "reativar" ? "reativar" : "desativar")
        );

        var verbo = d.verbo || "";
        function maiuscula(t) { return t.charAt(0).toUpperCase() + t.slice(1); }

        ref.titulo.textContent = d.titulo ||
            (bloqueado ? "Não é possível " + (verbo || (d.confirmar === "reativar" ? "reativar" : "desativar")) + " " + registro
                       : (verbo ? maiuscula(verbo) + " " + registro : tipo.titulo(registro)));

        // Mensagem: "Deseja desativar <strong>nome</strong>?" (nome como texto puro)
        ref.mensagem.textContent = "";
        if (d.mensagem) {
            ref.mensagem.textContent = d.mensagem;
        } else {
            ref.mensagem.appendChild(document.createTextNode(
                (verbo ? "Deseja " + verbo : tipo.mensagem) + " "
            ));
            ref.mensagem.appendChild(el("strong", "", nome));
            ref.mensagem.appendChild(document.createTextNode("?"));
        }

        if (bloqueado && !d.mensagem) {
            ref.mensagem.textContent = "Não é possível continuar com " + nome + ".";
        }

        ref.explicacao.textContent = d.explicacao ||
            (bloqueado ? "Existe uma pendência que impede esta ação." : tipo.explicacao);

        ref.confirmar.hidden = bloqueado;
        ref.cancelar.textContent = bloqueado ? "Entendi" : "Cancelar";

        ref.confirmar.className = "btn " + tipo.classe;
        ref.confirmar.textContent = "";
        var icone = el("i", "fa-solid " + tipo.icone);
        icone.setAttribute("aria-hidden", "true");
        ref.confirmar.appendChild(icone);
        ref.confirmar.appendChild(document.createTextNode(" " + (d.botao || (verbo ? maiuscula(verbo) : tipo.botao))));
        ref.confirmar.disabled = false;

        pendente = bloqueado ? null : { form: form };  // bloqueado: nunca envia
        gatilho = document.activeElement;

        dialogo.showModal();
        ref.cancelar.focus();            // foco inicial seguro
        // força o início da transição de abertura
        void dialogo.offsetWidth;
        dialogo.classList.add("is-aberto");

    }

    function fechar() {

        if (!dialogo || !dialogo.open || fechando) return;

        pendente = null;
        fechando = true;
        dialogo.classList.remove("is-aberto");

        var terminou = false;
        function concluir() {
            if (terminou) return;
            terminou = true;
            dialogo.close();
            fechando = false;
            if (gatilho && typeof gatilho.focus === "function" &&
                document.contains(gatilho)) {
                gatilho.focus();
            }
        }

        var caixa = dialogo.firstChild;
        caixa.addEventListener("transitionend", concluir, { once: true });
        setTimeout(concluir, 260);       // reserva (sem animação / reduced motion)

    }

    function confirmar() {

        if (!pendente) return;

        var form = pendente.form;
        pendente = null;
        ref.confirmar.disabled = true;   // evita duplo envio

        // form.submit() não dispara o evento "submit": sem laço.
        form.submit();

    }

    // Intercepta o envio de qualquer formulário marcado com data-confirmar.
    document.addEventListener("submit", function (e) {

        var form = e.target;

        if (!(form instanceof HTMLFormElement)) return;
        if (!form.hasAttribute("data-confirmar")) return;
        if (typeof HTMLDialogElement === "undefined") return; // navegador antigo: envia direto

        e.preventDefault();
        abrir(form);

    }, true);

})();
