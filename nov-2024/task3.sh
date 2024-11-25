k expose deployment/investigation-unit --type="NodePort" --port 80
k expose deployment/analysis-unit --type="NodePort" --port 80
k create deploy command-center --image=sachua/task-3:v0.0.1 --port 80
k logs -n default deployment/command-center | grep -im 1 culprit | sed 's/.*: //'
# Tan Ah Kow