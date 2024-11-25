cat <<EOF | k apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume
spec:
  persistentVolumeReclaimPolicy: Delete
  storageClassName: "local-path"
  hostPath:
    path: "/mnt/data"
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
EOF
cat <<EOF | k apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-claim
  namespace: default
spec:
  storageClassName: "local-path"
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF
cat <<EOF | k apply -f -
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pv-pod
  name: pv-pod
spec:
  containers:
    - name: pv-container
      image: sachua/task-2:v0.0.1
      volumeMounts:
        - mountPath: "/mnt/data"
          name: pv-storage
  volumes:
    - name: pv-storage
      persistentVolumeClaim:
        claimName: pv-claim
EOF
cat <<EOF | k apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analysis-unit
  namespace: default
  labels:
    run: pv-pod
spec:
  replicas: 1
  selector:
    matchLabels:
      run: pv-pod
  template:
    metadata:
      labels:
        run: pv-pod
      name: pv-pod
    spec:
      containers:
      - name: pv-container
        image: sachua/task-2:v0.0.1
        volumeMounts:
          - mountPath: "/mnt/data"
            name: pv-storage
      volumes:
      - name: pv-storage
        persistentVolumeClaim:
            claimName: pv-claim
EOF
k logs -n default deployment/analysis-unit | sed 1d | md5sum | awk '{print $1}'
# c33b083af53411171863163a79f6450c