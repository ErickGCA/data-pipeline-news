
kafka-topics --create --topic meu-topico-test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

kafka-topics --list --bootstrap-server localhost:9092

kafka-console-producer --topic meu-topico-test --bootstrap-server localhost:9092

kafka-console-consumer --topic meu-topico-test --bootstrap-server localhost:9092 --from-beginning

CD ~/pipelines-news

mkdir  (create diretory)

touch (create files)

cd .. (initial repository)

code . (open vscode)