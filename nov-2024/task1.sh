k create deploy investigation-unit --image=sachua/task-1:v0.0.1
k logs -n default deployment/investigation-unit | sed 's/.*: //'
# Katana