from constraint import Solver

class CspSolver(Solver):
    def backtracking(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        # A variável 'assignments' armazenará as atribuições de variáveis feitas até o momento.
        assignments = {}

        # A 'queue' será usada para armazenar as variáveis e seus respectivos valores, 
        # para que possamos realizar o backtracking caso uma atribuição falhe.
        queue = []

        while True:
            # 'unassigned_vars' armazena todas as variáveis que ainda não foram atribuídas.
            unassigned_vars = [v for v in domains if v not in assignments]

            # Se não houver mais variáveis não atribuídas, significa que encontramos uma solução.
            if not unassigned_vars:
                yield assignments.copy()  # Retorna a atribuição encontrada.
                if not queue:
                    return  # Se não houver mais nada na fila, terminamos a execução.

                # Se a fila tiver alguma variável, voltamos para tentar outra possibilidade.
                variable, values, pushdomains = queue.pop()
                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()  # Restaura o estado dos domínios.
                continue

            # Função heurística que calcula o critério de escolha da próxima variável a ser atribuída.
            def heuristic_key(var):
                # 'domain_size' é o número de valores possíveis para a variável.
                domain_size = len(domains[var])
                # 'degree' conta o número de restrições com outras variáveis ainda não atribuídas.
                degree = sum(
                    1 for constraint, vars_in_constraint in vconstraints.get(var, [])
                    if any(v != var and v not in assignments for v in vars_in_constraint)
                )
                # Retorna uma tupla que prioriza variáveis com menor domínio e maior grau de restrições.
                return (domain_size, -degree)

            # Seleciona a variável com base na heurística: variável com o menor domínio e maior grau de restrições.
            variable = min(unassigned_vars, key=heuristic_key)

            # 'values' é uma cópia dos valores possíveis para a variável selecionada.
            values = domains[variable][:]
            # 'pushdomains' guarda os domínios das variáveis vizinhas que ainda não foram atribuídas.
            pushdomains = [domains[x] for x in domains if x not in assignments and x != variable]

            while True:
                if not values:
                    print(f"Backtracking em: {variable}")  # Imprime a variável que está sendo processada.
                    # Se não há mais valores para a variável, começamos o backtracking.
                    del assignments[variable]  # Desfaz a atribuição feita.
                    while queue:
                        # Tenta desfazer as últimas atribuições até encontrar uma possibilidade válida.
                        variable, values, pushdomains = queue.pop()
                        if pushdomains:
                            for domain in pushdomains:
                                domain.popState()
                        if values:
                            break  # Se encontramos um valor válido, continuamos.
                        
                        del assignments[variable]  # Se não, continua o backtracking.
                    else:
                        return  # Se não houver mais alternativas, o problema não tem solução.

                # Atribui um valor à variável e imprime o progresso.
                assignments[variable] = values.pop()
                print(f"Insert {variable} = {assignments[variable]}")

                # Restaura o estado dos domínios de variáveis vizinhas.
                if pushdomains:
                    for domain in pushdomains:
                        domain.pushState()

                # Verifica se a atribuição feita não viola nenhuma restrição.
                for constraint, variables in vconstraints[variable]:
                    if not constraint(variables, domains, assignments, pushdomains):
                        print(f"Removed {variable} = {assignments[variable]}")
                        break  # Se a atribuição viola alguma restrição, desfazemos a atribuição.
                else:
                    # Se todas as restrições foram satisfeitas, sai do loop.
                    break

                # Restaura o estado dos domínios se necessário.
                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            # Adiciona a variável com o valor atribuído de volta na fila para possível backtracking.
            queue.append((variable, values, pushdomains))


    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        iter = self.backtracking(domains, constraints, vconstraints)
        try:
            return next(iter)
        except StopIteration:
            return None