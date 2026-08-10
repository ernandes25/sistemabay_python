from tarefas.models import PlanoTarefaItem

def buscar_tarefas_da_empresa(empresa):
    if not empresa.plano_tarefas:
        return []
    
    itens_do_plano = PlanoTarefaItem.objects.filter(
        plano=empresa.plano_tarefas,
        ativo=True
    )
    return itens_do_plano
        


    
    


    
        
        


    