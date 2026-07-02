(function () {
    const camposExecucao = [
        'controla_execucao',
        'tipo_dia_execucao',
        'dia_execucao',
        'meses_apos_competencia_execucao',
        'ajuste_dia_execucao_nao_util',
        'dias_antecedencia_alerta_execucao',
    ];
    const camposVencimentoRecorrente = [
        'tipo_dia_vencimento',
        'dia_vencimento',
        'meses_apos_competencia',
        'ajuste_dia_nao_util',
        'dias_antecedencia_alerta',
        'inicio_competencia',
    ];

    function campoPorNome(nome) {
        return document.getElementById(`id_${nome}`);
    }

    function linhaDoCampo(nome) {
        const campo = campoPorNome(nome);

        if (!campo) {
            return null;
        }

        return document.querySelector(`.form-row.field-${nome}`) || campo.closest('.form-row');
    }

    function marcarCampoComoInativo(nome, inativo) {
        const campo = campoPorNome(nome);
        const linha = linhaDoCampo(nome);

        if (!campo || !linha) {
            return;
        }

        linha.classList.toggle('campo-inativo-subtarefa', inativo);
        linha.style.opacity = inativo ? '0.45' : '';
        linha.style.backgroundColor = inativo ? '#f5f5f5' : '';
        campo.disabled = inativo;
        campo.tabIndex = inativo ? -1 : 0;
    }

    function filtrarTarefasPrincipaisPorDepartamento() {
        const departamento = campoPorNome('departamento');
        const tarefaPrincipal = campoPorNome('tarefa_principal');

        if (!departamento || !tarefaPrincipal) {
            return;
        }

        Array.from(tarefaPrincipal.options).forEach(function (option) {
            const departamentoTarefa = option.dataset.departamento || '';
            const deveMostrar = !option.value || !departamento.value || departamentoTarefa === departamento.value;

            option.hidden = !deveMostrar;
            option.disabled = !deveMostrar;
        });

        if (tarefaPrincipal.selectedOptions.length && tarefaPrincipal.selectedOptions[0].disabled) {
            tarefaPrincipal.value = '';
        }
    }

    function atualizarCamposPorNatureza() {
        const natureza = campoPorNome('natureza');

        if (!natureza) {
            return;
        }

        const ehPrincipal = natureza.value === 'PRINCIPAL';
        const ehSubtarefa = natureza.value === 'SUBTAREFA';
        const controlaExecucao = campoPorNome('controla_execucao');

        camposExecucao.forEach(function (nome) {
            marcarCampoComoInativo(nome, !ehPrincipal);
        });

        camposVencimentoRecorrente.forEach(function (nome) {
            marcarCampoComoInativo(nome, ehPrincipal);
        });

        marcarCampoComoInativo('tarefa_principal', !ehSubtarefa);

        if (!ehSubtarefa) {
            const tarefaPrincipal = campoPorNome('tarefa_principal');

            if (tarefaPrincipal) {
                tarefaPrincipal.value = '';
            }
        }

        filtrarTarefasPrincipaisPorDepartamento();

        if (controlaExecucao) {
            controlaExecucao.checked = ehPrincipal;
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        atualizarCamposPorNatureza();

        const natureza = campoPorNome('natureza');
        const departamento = campoPorNome('departamento');

        if (natureza) {
            natureza.addEventListener('change', atualizarCamposPorNatureza);
        }

        if (departamento) {
            departamento.addEventListener('change', filtrarTarefasPrincipaisPorDepartamento);
        }
    });
})();
