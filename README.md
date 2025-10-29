1. Geração Automática de Códigos
Os códigos são gerados automaticamente no formato "XX000YY", onde "XX" são as duas primeiras letras da classe, "000" é um número sequencial (incrementado a cada novo registro) e "YY" são as duas últimas letras da classe.
Cliente: codigoCliente (ex: "CL001TE")
Corretor: codigoCorretor (ex: "CO001OR")
Imóvel: codigoImovel (ex: "IM001EL")
Proprietário: codigoProprietario (ex: "PR001IO")
Transação: codigoTransacao (ex: "TR001AO")
Visita: codigoVisita (ex: "VI001TA")

2. Regras de Negócio de Transações
As transações de imóveis são regidas por um conjunto de validações e lógicas específicas:
Imóvel em Transação Ativa:
Não é permitido cadastrar uma nova transação (seja venda ou aluguel) para um imóvel que já possua uma transação.
Disponibilidade para Locação:
Uma transação de aluguel só pode ser criada se o imóvel estiver marcado como disponível.
Cálculo de Comissão:
A comissão do corretor é calculada com base no tipo de transação e na característica do imóvel (zona_valorizacao):
Venda:
Imóvel em "Zona de Valorização": Comissão de 7% sobre o valor de venda.
Demais imóveis: Comissão de 5% sobre o valor de venda.
Aluguel:
Imóvel em "Zona de Valorização": Comissão de 10% sobre o valor de venda.
Demais imóveis: Comissão de 8% sobre o valor de venda.
Exclusão de Visitas Após Venda: Quando uma transação de venda é salva, todas as visitas futuras agendadas para o imóvel em questão, a partir da data, são automaticamente removidas.
Restrição de Alteração do Valor de Venda: O valor de venda de um imóvel não pode ser modificado se houver uma transação associada a ele.

3. Regras de Negócio de Visitas
Agendamento em Imóvel com Venda Pendente: Não é permitido agendar visitas para um imóvel se estiver "Em Confirmação de Venda".
Conflito de Horário do Corretor: Um corretor não pode ter múltiplas visitas agendadas para o mesmo imóvel no mesmo dia com um intervalo menor que 30 minutos entre elas.
Data de Agendamento: A data para agendamento de uma visita deve ser igual ou posterior à data atual.

4. Regras de Negócio de Imóveis
Validação de Áreas:
A área privativa não pode ser maior que a área total.
A área útil não pode ser maior que a área total.
Status do Imóvel: O status do imóvel é dinâmico:
"Em Confirmação de Venda": Se houver uma transação de venda pendente para o imóvel.
"Não Disponível para Locação": Se o atributo disponível locação for falso.
Valorização do Imóvel: Se um imóvel estiver em uma zona valorização, seu valor de venda é ajustado em 10%.
Imóvel Desatualizado: Um imóvel é considerado "desatualizado" se a data da sua última atualização for anterior a seis meses da data atual.
Restrições de Exclusão: Não é possível excluir um imóvel se existirem visitas ou transações associadas a ele.

5. Regras de Negócio de Pessoas (Cliente, Corretor, Proprietário)
As entidades que representam pessoas no sistema (Cliente, Corretor, Proprietário) compartilham algumas regras de negócio essenciais:
Formato de Telefone: O campo telefone aceita 10 ou 11 dígitos numéricos (incluindo o DDD) e é automaticamente formatado para (DD) XXXXX-XXXX ou (DD) XXXX-XXXX.
Unicidade do E-mail: O campo e-mail deve ser único para cada pessoa cadastrada no sistema.




































































