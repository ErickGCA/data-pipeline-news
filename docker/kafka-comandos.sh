# Criar tópico
kafka-topics --create --topic meu-topico-test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Listar tópicos
kafka-topics --list --bootstrap-server localhost:9092

# Produzir mensagens
kafka-console-producer --topic meu-topico-test --bootstrap-server localhost:9092

# Consumir mensagens
kafka-console-consumer --topic meu-topico-test --bootstrap-server localhost:9092 --from-beginning

